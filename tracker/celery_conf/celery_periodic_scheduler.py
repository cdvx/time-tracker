from celery.schedules import crontab
from tracker.services import celery_scheduler

celery_scheduler.conf.beat_schedule = {
        'run-get-daily-logged-time': {
        'task': 'get_daily_logged_time',
        # run everyday at 1 minute passed midnight
        'schedule': crontab(minute='*')# crontab(minute=1, hour=0),
    }
}

