from celery import Celery
from celerybeat_schedule import beat_schedule

celery = Celery('photo-collage-tool',
                broker='redis://localhost:6379/0',
                backend='redis://localhost:6379/0',
                include=['tasks'])

celery.conf.beat_schedule = beat_schedule
celery.conf.timezone = 'UTC'
