from celery.schedules import crontab
from api.services import celery_scheduler

celery_scheduler.conf.beat_schedule = {
        'run-get-daily-logged-time': {
        'task': 'get_daily_logged_time',
        # run everyday at 1 minute passed midnight
        'schedule': crontab(minute=1, hour=0),
    },
    'run-rest-logs-daily': {
        'task': 'reset_logs',
        # run everyday at 4 minutes passed midnight
        'schedule': crontab(minute=4, hour=0),
    }
}

