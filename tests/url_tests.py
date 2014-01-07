import json

from . import BaseTestCase


class URLTest(BaseTestCase):

    def test_blog_requests(self):
        response = self.client.get('/blog/test/new/routes/abc')
        assert response.status_code == 200

        response = self.client.get('/blog/page/page-slug')
        assert response.status_code == 200
        json_data = response.content.decode('utf-8')
        assert {'page_slug':'page-slug'} == json.loads(json_data)

    def test_dashboard_requests(self):
        response = self.client.get('/dashboard')
        assert response.status_code == 200
        assert response.content.decode('utf-8').strip() == 'Dashboard GET'

        # Test POST to the same URL
        response = self.client.post('/dashboard')
        assert response.status_code == 200
        assert response.content.decode('utf-8').strip() == 'Dashboard POST'

        # Test PUT to the same URL
        response = self.client.put('/dashboard')
        assert response.status_code == 200
        assert response.content.decode('utf-8').strip() == 'Dashboard PUT'

    def test_non_rhetoric_urls(self):
        response = self.client.get('/admin/')
        assert response.status_code == 200

    def test_route_path(self):
        url = self.rhetoric.url.route_path('index.dashboard')
        assert url == '/dashboard'
