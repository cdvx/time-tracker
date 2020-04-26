"""Module to run application"""

#local imports
from config import AppConfig
from main import celery_app, create_app

app = create_app(AppConfig)


if __name__ == '__main__':
    app.run(host=AppConfig.HOST, port=AppConfig.PORT)
