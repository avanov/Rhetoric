import json

from . import BaseTestCase


class FormValidationTest(BaseTestCase):

    def test_validate_form(self):
        response = self.client.post('/articles/en')
        assert response.status_code == 200

        json_data = json.loads(response.content.decode('utf-8'))
        assert json_data['ok'] is False
        assert json_data['message'] == 'Form validation error.'
