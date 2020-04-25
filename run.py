from main import celery_app, create_app
from config import AppConfig


app = create_app(AppConfig)


if __name__ == '__main__':
    app.run(host=AppConfig.HOST, port=5000)