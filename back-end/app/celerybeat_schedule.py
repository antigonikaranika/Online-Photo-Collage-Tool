from celery.schedules import crontab

beat_schedule = {
    'cleanup-every-30-minutes': {
        'task': 'tasks.cleanup_old_files',
        'schedule': crontab(minute='*/30'),  # Every 30 minutes
        'args': ()
    }
}
