from flask import Flask
from celery import Celery
from config import AppConfig


celery_app = Celery(__name__)

def create_app(config=AppConfig):
    """Return app object given config object."""
    app = Flask(__name__)
    app.config.from_object(config)
    celery_app.config_from_object(config)

    TaskBase = celery_app.Task
    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs) 
    celery_app.Task = ContextTask

    app.url_map.strict_slashes = False

    from api.time_log import time_log

    app.register_blueprint(time_log)

    # register celery tasks
    import celery_conf.tasks

    return app