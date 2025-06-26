from celery import Celery
import os
import time

celery = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@celery.task(bind=True)
def process_collage_task(self, image_paths, collage_type, border_size, border_color):
    from utils.image_processing import resize_images, combine_images

    try:
        resized_images = resize_images(image_paths, collage_type)
        collage_id, final_collage_path = combine_images(resized_images, collage_type, border_size, border_color)

        return {'status': 'completed', 'collage_id': collage_id, 'collage_path': final_collage_path}

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
