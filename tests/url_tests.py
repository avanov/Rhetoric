from . import BaseTestCase


class URLTest(BaseTestCase):

    def test_requests(self):
        response = self.client.get('/blog/test/new/routes/abc')
        assert response.status_code == 200

    def test_dashboard_requests(self):
        response = self.client.get('/dashboard')
        assert response.status_code == 200
        assert response.content.strip() == 'Dashboard'

    def test_non_rhetoric_urls(self):
        response = self.client.get('/admin/')
        assert response.status_code == 200
