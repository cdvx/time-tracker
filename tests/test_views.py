"""Module for testing views"""
import os

from api.storage import DataStore
BASE_URL = os.getenv('BASE_URL')

class TestTimeLogViews:
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
