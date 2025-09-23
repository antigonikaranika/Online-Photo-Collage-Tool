from celery_config import celery


# Run this file to start the Celery worker:
# celery -A worker.celery worker --loglevel=info

# Nothing else is needed here because celery is already configured in app.py
