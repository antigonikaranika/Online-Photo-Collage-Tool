from flask import Flask, request, jsonify
from celery import Celery
import os
from werkzeug.utils import secure_filename
import uuid
from celery.result import AsyncResult

# Flask app initialization
app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

from tasks import process_collage_task  # Import the Celery task


@app.route('/create-task', methods=['POST'])
def create_task():
    # Retrieve files and form data
    files = request.files.getlist('images')
    collage_type = request.form.get('collage_type')  # 'horizontal' or 'vertical'
    border_size = int(request.form.get('border_size', 0))
    border_color = request.form.get('border_color', '#000000')  # Default black

    if not files:
        return jsonify({'error': 'No files provided.'}), 400

    saved_paths = []
    for file in files:
        if file:
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            saved_paths.append(file_path)

    # Send task to Celery
    task = process_collage_task.apply_async(args=[saved_paths, collage_type, border_size, border_color])

    return jsonify({'task_id': task.id}), 202

@app.route('/task-status/<task_id>', methods=['GET'])
def task_status(task_id):
    task_result = AsyncResult(task_id, app=celery)

    response = {'task_id': task_id, 'state': task_result.state}

    if task_result.state == 'PENDING':
        response['status'] = 'Task is pending in the queue.'

    elif task_result.state == 'STARTED':
        response['status'] = 'Task is currently being processed.'

    elif task_result.state == 'SUCCESS':
        response['status'] = 'Task completed successfully.'
        response['result'] = task_result.result  

    elif task_result.state == 'FAILURE':
        response['status'] = 'Task failed.'
        response['error'] = str(task_result.result)

    else:
        response['status'] = 'Task is in an unknown state.'

    return jsonify(response)

from flask import send_from_directory

@app.route('/get-collage/<collage_id>', methods=['GET'])
def get_collage(collage_id):
    collage_folder = 'static/collages'
    filename = f'collage_{collage_id}.jpg'

    try:
        return send_from_directory(collage_folder, filename)
    except FileNotFoundError:
        return jsonify({'error': 'Collage not found.'}), 404

if __name__ == '__main__':
    app.run(debug=True)

