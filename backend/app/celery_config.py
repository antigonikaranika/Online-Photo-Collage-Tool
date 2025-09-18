import os
from dotenv import load_dotenv
load_dotenv()

from celery import Celery
from backend.app.celerybeat_schedule import beat_schedule

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

celery = Celery('photo-collage-tool',
                broker=redis_url,
                backend=redis_url,
                include=['backend.app.tasks'])

# Configure Celery Beat
celery.conf.beat_schedule = beat_schedule
celery.conf.timezone = 'UTC'
