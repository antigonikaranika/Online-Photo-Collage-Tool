import os
import uuid
import time
from celery_config import celery
from utils.image_processing import resize_images, combine_images

@celery.task(name='tasks.process_collage_task')
def process_collage_task(image_paths, collage_type, border_size, border_color):
    try:
        # Make sure input paths are absolute
        image_paths = [os.path.abspath(path) for path in image_paths]

        # Step 1: Resize images
        resized_images = resize_images(image_paths, collage_type)

        # Step 2: Create collage filename and path
        collage_id = str(uuid.uuid4())
        collage_filename = f'collage_{collage_id}.jpg'
        collage_folder = os.path.abspath('static/collages')
        os.makedirs(collage_folder, exist_ok=True)

        final_collage_path = os.path.join(collage_folder, collage_filename)

        # Step 3: Combine images and save the final collage
        combine_images(resized_images, collage_type, border_size, border_color, final_collage_path)

        return {'status': 'completed', 'collage_id': collage_id}

    except Exception as e:
        return {'status': 'failed', 'error': str(e)}


@celery.task
def cleanup_old_files(directory='static/collages', max_age_seconds=3600):
    """Delete files older than max_age_seconds (default: 1 hour)."""
    now = time.time()

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_age = now - os.path.getmtime(file_path)
            if file_age > max_age_seconds:
                try:
                    os.remove(file_path)
                    print(f"Deleted old file: {file_path}")
                except Exception as e:
                    print(f"Error deleting file {file_path}: {str(e)}")
