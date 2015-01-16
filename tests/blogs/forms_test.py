import json

from .. import BaseTestCase


class BlogsFormTest(BaseTestCase):
    def test_json_body_request(self):
        response = self.client.post('/blog/page/page-slug',
                          content_type='application/json',
                          data=json.dumps({'slug': 'slug'}))
        assert response.status_code == 200
