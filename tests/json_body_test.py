import json
from . import BaseTestCase


class JSONBodyTest(BaseTestCase):

    def test_api_version_requests(self):
        response = self.client.post('/json-body', data=json.dumps({'key': 'value'}), content_type='application/json')
        assert response.status_code == 200
