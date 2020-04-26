"""Module to set up celery worker"""

# local imports
from config import AppConfig
from main import celery_app, create_app

app = create_app(config=AppConfig)
app.app_context().push()
