from flask import Flask, request, jsonify, send_from_directory
import os

from dotenv import load_dotenv
load_dotenv()

from werkzeug.utils import secure_filename
import uuid
from celery.result import AsyncResult
from celery_config import celery

# Flask app initialization
app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

IS_DOCKER = os.getenv('IS_DOCKER', '1') == '1'

# Use REDIS_URL environment variable or default to localhost for local dev
app.config['broker_url'] = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
app.config['result_backend'] = os.getenv('REDIS_URL', 'redis://localhost:6379/0')


celery.conf.update(app.config)

# ----------------------------
# Create Collage Task Endpoint
# ----------------------------
@app.route('/create-task', methods=['POST'])

def create_task():
    files = request.files.getlist('images')
    collage_type = request.form.get('collage_type')
    border_size = int(request.form.get('border_size', 0))
    border_color = request.form.get('border_color', '#000000')

    if not files:
        return jsonify({'error': 'No files provided.'}), 400

    saved_paths = []
    for file in files:
        if file:
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            upload_folder_absolute = os.path.abspath(app.config['UPLOAD_FOLDER'])

            file_path = os.path.join(upload_folder_absolute, unique_filename)
            file.save(file_path)
            saved_paths.append(file_path)

    # Use task name to avoid circular import
    task = celery.send_task('tasks.process_collage_task', args=[saved_paths, collage_type, border_size, border_color])

    return jsonify({'task_id': task.id}), 202

# -----------------------------
# Task Status Check Endpoint
# -----------------------------
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

# -----------------------------
# Get Collage by ID Endpoint
# -----------------------------
@app.route('/get-collage/<collage_id>', methods=['GET'])
def get_collage(collage_id):
    collage_folder = 'static/collages'
    filename = f'collage_{collage_id}.jpg'

    try:
        return send_from_directory(collage_folder, filename)
    except FileNotFoundError:
        return jsonify({'error': 'Collage not found.'}), 404

# Serve Frontend Files

import shutil

@app.route('/')
def serve_index():
    uploads_folder = os.path.abspath('static/uploads')
    collages_folder = os.path.abspath('static/collages')

    try:
        # Remove all files in uploads folder
        for filename in os.listdir(uploads_folder):
            file_path = os.path.join(uploads_folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
    except Exception as e:
        print(f"[Warning] Could not clean uploads folder: {e}")

    try:
        # Remove all files in collages folder
        for filename in os.listdir(collages_folder):
            file_path = os.path.join(collages_folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
    except Exception as e:
        print(f"[Warning] Could not clean collages folder: {e}")

    if IS_DOCKER:
        # In Docker:
        return send_from_directory('frontend', 'index.html')
    else:
        # Local: 
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
        return send_from_directory(os.path.join(project_root, 'frontend'), "index.html")


@app.route('/<path:filename>')
def serve_static_files(filename):
    if IS_DOCKER:
        # In Docker: 
        return send_from_directory('frontend', filename)
    else:
        # Local: 
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
        return send_from_directory(os.path.join(project_root, 'frontend'), filename)


# -----------------------------
# Run Flask
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
