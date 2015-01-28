import unittest
import json
from . import BaseTestCase


class URLTest(BaseTestCase):

    @unittest.skip('No longer part of Rhetoric')
    def test_match_api_version(self):
        # from rhetoric.predicates import match_api_version
        #
        # assert match_api_version('1.0', '1.0') is True
        # assert match_api_version('1.0', '1.00') is True
        # assert match_api_version('1.0', '1.0.0') is True
        # assert match_api_version('1', '1.0.0') is True
        #
        # assert match_api_version('1.0', '1.01') is False
        # assert match_api_version('1.0', '1.0.1') is False
        #
        # assert match_api_version('1.0', '==1.01') is False
        # assert match_api_version('1.0', '==1.0.1') is False
        #
        # assert match_api_version('1.0', '>=1.0') is True
        # assert match_api_version('1.0', '>=1.0.0') is True
        #
        # assert match_api_version('1.0.1', '>=1.0') is True
        # assert match_api_version('1.1', '>=1.1.0') is True
        #
        # assert match_api_version('1.0.1', '<=1.0') is False
        # assert match_api_version('1.1', '<1.1.0') is False
        #
        # assert match_api_version('1.0.1', '>1.0') is True
        # assert match_api_version('1.1', '>1.1.0') is False
        pass


    def test_api_version_requests(self):
        response = self.client.get('/versions')
        assert response.status_code == 200
        assert json.loads(response.content.decode('utf-8')) == {'version': '1.0'}

        # GET vs POST with versioning
        # ---------------------------
        response = self.client.get('/versions', **{'X-API-VERSION': '1.1'})
        assert response.status_code == 200
        assert json.loads(response.content.decode('utf-8')) == {'method': 'GET', 'version': '>1.0, <2.0'}

        response = self.client.post('/versions', **{'X-API-VERSION': '1.1'})
        assert response.status_code == 200
        assert json.loads(response.content.decode('utf-8')) == {'method': 'POST', 'version': '>1.0, <2.0'}

        # v2
        # ---------------------------
        response = self.client.post('/versions', **{'X-API-VERSION': '2.1'})
        assert response.status_code == 200
        assert json.loads(response.content.decode('utf-8')) == {'version': '>=2.0'}

