"""Module for configuration"""

import os
import sys

class Config:
    """Base Config class"""
    PORT = os.getenv('PORT')
    HOST = os.getenv('HOST', 'localhost')
    APP_TOKEN = os.getenv('APP_TOKEN')
    AUTH_TOKEN = os.getenv('AUTH_TOKEN')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    REDIS_URL = os.getenv('REDIS_URL', default='redis://localhost:6379/0')
    ORGANIZATIONS = os.path.join(os.path.dirname(__file__), 'api/storage', os.getenv('ORGANIZATIONS'))
    PROJECTS = os.path.join(os.path.dirname(__file__), 'api/storage', os.getenv('PROJECTS')) #ACTIVITY
    ACTIVITIES = os.path.join(os.path.dirname(__file__), 'api/storage', os.getenv('ACTIVITIES'))
    MAIL_SERVER =  os.getenv('HOST', 'localhost')
    MAIL_PORT = os.getenv('MAIL_PORT', 25)
    SERVER_NAME = '127.0.0.1:5000'
    MAIL_USE_SSL = True


class DevelopmentConfig(Config):
    """Development DevelopmentConfig class"""
    DEBUG = True

class TestingConfig(Config):
    """Development DevelopmentConfig class"""
    DEBUG = True
    TESTING = True

class ProductionConfig(Config):
    """Development ProductionConfig class"""
    DEBUG = False
    TESTING = False


# config dict
app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'prodcution': ProductionConfig
}

AppConfig = TestingConfig if 'pytest' in sys.modules else app_config.get(
    os.getenv('FLASK_ENV'), DevelopmentConfig)
