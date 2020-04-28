"""Module for setting up testing fixtures"""

# Third-party libraries
import pytest
from flask import current_app, Response, template_rendered
from unittest.mock import Mock

# Local imports
from main import create_app
from tracker.storage import DataStore
from tracker.utils import Util

from tracker.celery_conf.tasks import (
    get_daily_activity,
    get_daily_logged_time, 
    get_daily_projects, send_email
)

from config import app_config

@pytest.yield_fixture(scope='session')
def test_app():
    """
    Setup flask test app, this only gets executed once.
    Args:
        None
    Returns:
        Flask app
    """
    _app = create_app(config=app_config['testing'])

    return _app

@pytest.fixture(scope='function')
def client(test_app):
    """
    Setup an app client, this gets executed for each test function.
    Args:
        app_(obj): Pytest fixture
    Returns:
        Flask app client
    """
    yield test_app.test_client()

@pytest.fixture
def captured_templates(test_app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, test_app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, test_app)

@pytest.fixture(scope='function')
def mock_write_to_file(monkeypatch):
    monkeypatch.setattr(
        Util, 'write_to_file',
        lambda x,y: None)

@pytest.fixture(scope='function')
def mock_get_daily_projects(monkeypatch):
    monkeypatch.setattr(
        get_daily_projects, 'delay',
        lambda : None)

@pytest.fixture(scope='function')
def mock_get_daily_activity(monkeypatch):
    monkeypatch.setattr(
        get_daily_activity, 'delay',
        lambda : None)
