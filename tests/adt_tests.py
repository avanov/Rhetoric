from . import BaseTestCase


class ADTTest(BaseTestCase):

    def test_metadata(self):
        from tests.testapp.testapp import types

        assert types.Language.ENGLISH.variant_of.__adt__['variants'] == {'ENGLISH', 'GERMAN'}
        assert types.Language.ENGLISH.variant_of == types.Language
        assert types.Language.ENGLISH.value == 'en'
