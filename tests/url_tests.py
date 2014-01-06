from . import BaseTestCase




class URLTest(BaseTestCase):
    def test_search_quotes(self):

        rv = self.rhetoric.url.search_quotes("/url")
        assert rv is None
