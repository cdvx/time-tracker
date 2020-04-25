from celery.schedules import crontab
from api.services import celery_scheduler

celery_scheduler.conf.beat_schedule = {
        'run-get-daily-logged-time': {
        'task': 'get_daily_logged_time',
        # 'schedule': crontab(minute=1, hour=0),
        'schedule': crontab(minute="*")
    }
}

