"""Module for setting up testing fixtures"""

# Third-party libraries
import pytest
from flask import current_app, Response, template_rendered

# Local imports
from main import create_app
from api.storage import DataStore

# constants
from config import app_config

@pytest.yield_fixture(scope='session')
def app_():
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
def client(app_):
    """
    Setup an app client, this gets executed for each test function.
    Args:
        app_(obj): Pytest fixture
    Returns:
        Flask app client
    """
    yield app_.test_client()

@pytest.fixture
def captured_templates(app_):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app_)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app_)