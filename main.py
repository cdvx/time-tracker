from flask import Flask
from celery import Celery
from config import AppConfig
from flask_mail import Mail
from flask_cors import CORS

import os


celery_app = Celery(__name__)
mail = Mail()

def create_app(config=AppConfig):
    """Return app object given config object."""
    app = Flask(__name__)
    app.config.from_object(config)
    celery_app.config_from_object(config)

    app.config.update(dict(
        DEBUG = True,
        MAIL_SERVER = 'smtp.gmail.com',
        MAIL_PORT = 587,
        MAIL_USE_TLS = True,
        MAIL_USE_SSL = False,
        MAIL_USERNAME = os.getenv('MAIL_USERNAME'),
        MAIL_PASSWORD = os.getenv('MAIL_PASSWORD'),
        MAIL_DEFAULT_SENDER = os.getenv('MAIL_PASSWORD'),
    ))
    mail.init_app(app)
    CORS(app)

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