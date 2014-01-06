from . import BaseTestCase


class URLTest(BaseTestCase):

    def test_routes(self):
        from tests.testapp.testapp import urls

        pattern_list = urls.urlpatterns
        route_names = {p.name for p in pattern_list}
        self.assertIn('test.new.routes', route_names)
