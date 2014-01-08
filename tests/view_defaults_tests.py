import json

from . import BaseTestCase


class ViewDefaultsTest(BaseTestCase):

    def test_requests_v1(self):
        # GET v1
        response = self.client.get('/api/dashboard/')
        assert response.status_code == 200
        json_data = json.loads(response.content.decode('utf-8'))
        assert json_data == {'version': 1, 'method': 'GET'}

        # POST v1
        response = self.client.post('/api/dashboard/')
        assert response.status_code == 200
        json_data = json.loads(response.content.decode('utf-8'))
        assert json_data == {'version': 1, 'method': 'POST'}

    def test_requests_v2(self):
        # GET v2
        response = self.client.get('/api/dashboard/', **{'X-API-VERSION': '2.0'})
        assert response.status_code == 200
        json_data = json.loads(response.content.decode('utf-8'))
        assert json_data == {'version': 2, 'method': 'GET'}

        # POST v2
        response = self.client.post('/api/dashboard/', **{'X-API-VERSION': '2.0'})
        assert response.status_code == 200
        json_data = json.loads(response.content.decode('utf-8'))
        assert json_data == {'version': 2, 'method': 'POST'}

    def test_requests_non_existing(self):
        # GET non-existing
        response = self.client.get('/api/dashboard/', **{'X-API-VERSION': '0.1'})
        assert response.status_code == 404
