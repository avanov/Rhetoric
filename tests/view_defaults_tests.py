import json

from . import BaseTestCase


class URLTest(BaseTestCase):

    def test_requests(self):
        response = self.client.get('/api/dashboard/')
        assert response.status_code == 200
        json_data = json.loads(response.content.decode('utf-8'))
        assert json_data == {'method': 'GET'}
