"""Module for scheduling configuration"""

# 3rd party libraries
from celery.schedules import crontab

# local imports
from tracker.services import celery_scheduler

celery_scheduler.conf.beat_schedule = {
        'run-get-daily-logged-time': {
        'task': 'get_daily_logged_time',
        # run everyday at 1 minute passed midnight
        'schedule': crontab(minute=1, hour=0),
    }
}
