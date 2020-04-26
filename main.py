"""Module for app factory"""

# system libraries
import os

# 3rd party libraries
from celery import Celery
from flask import Flask
from flask_cors import CORS
from flask_mail import Mail

# local imports
from config import AppConfig

celery_app = Celery(__name__)
mail = Mail()

dir_path = os.path.dirname(os.path.realpath(__file__))

def create_app(config=AppConfig):
    """Instantiate and return Flask app."""

    app = Flask(__name__, root_path=f'{dir_path}/public/')
    app.config.from_object(config)
    celery_app.config_from_object(config)

    # configure mail settings
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

    # register time_log blueprint
    from tracker.api.time_log import time_log
    app.register_blueprint(time_log)

    # register celery tasks
    import tracker.celery_conf.tasks

    return app
