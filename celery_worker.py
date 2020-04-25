from config import *
from main import create_app, celery_app

app = create_app(config=AppConfig)
app.app_context().push()
