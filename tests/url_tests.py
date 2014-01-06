from . import BaseTestCase


class URLTest(BaseTestCase):

    def test_routes(self):
        from tests.testapp.testapp import urls

        pattern_list = urls.urlpatterns
        route_names = {p.name for p in pattern_list}
        self.assertIn('test.new.routes', route_names)

    def test_requests(self):
        response = self.client.get('/blog/test/new/routes/abc')
        assert response.status_code == 200
