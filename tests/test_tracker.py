"""Module for testing views"""
import os

from unittest.mock import Mock, patch


from .conftest import *
BASE_URL = os.getenv('BASE_URL')

class ResponseData:
    def __init__(self):
        self.json = lambda: {}

class TestTracker:
    """Test class for endpoints"""
    store = DataStore()


    def test_get_logged_time(self, client, captured_templates):
        res = client.get(BASE_URL)
        assert res.status_code == 200
       
        template, context = captured_templates[0]
        assert template.name == "table.html"
        assert context['data'] == self.store.get_data()[0]

    def test_inspect_data(self, client):
        res = client.get(f'{BASE_URL}/inspect')
        assert res.status_code == 200
       
        assert res.json[0] == self.store.get_data()[0]


    @patch('tracker.celery_conf.tasks.requests.get')
    @pytest.mark.celery(result_backend='redis://', broker='redis://')
    def test_get_daily_logged_time(self, mock_get, mock_write_to_file,mock_get_daily_activity, mock_get_daily_projects):
        mock_get.return_value = ResponseData()
        value = get_daily_logged_time()

        assert value is None

    @patch('tracker.celery_conf.tasks.mail.send')
    @pytest.mark.celery(result_backend='redis://', broker='redis://')
    def test_send_email(self, mock_send,test_app):
        mock_send.return_value = None
        with test_app.app_context():
            value = send_email('email', {},'date')

        assert value is None

    @patch('tracker.celery_conf.tasks.requests.get')
    @pytest.mark.celery(result_backend='redis://', broker='redis://')
    def test_get_daily_projects(self, mock_get, mock_write_to_file):
        mock_get.return_value = ResponseData()
        value = get_daily_projects()

        assert value is None

    @patch('tracker.celery_conf.tasks.requests.get')
    @pytest.mark.celery(result_backend='redis://', broker='redis://')
    def test_get_daily_activity(self, mock_get, mock_write_to_file):
        mock_get.return_value = ResponseData()
        value = get_daily_activity()

        assert value is None
