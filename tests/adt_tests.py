from decimal import Decimal

from . import BaseTestCase


class ADTTest(BaseTestCase):

    def test_metadata(self):
        from tests.testapp.testapp import types

        assert types.Language.ENGLISH.variant_of == types.Language
        assert types.Language.ENGLISH.value == 'en'

    def test_match(self):
        from tests.testapp.testapp import types

        assert types.Language.match('en')
        self.assertRaises(types.Language.Mismatch, types.Language.match, 'ru')

    def test_trading_app_match(self):
        from tests.testapp.testapp.trading import models

        order = models.Order(tid=1, price=Decimal('1.0000'), size=1)
        instruction_strategy = models.Instruction.match(order)
        assert isinstance(instruction_strategy, dict)

    def test_trading_app_filter(self):
        from tests.testapp.testapp.trading import models
        from tests.testapp.testapp.trading import logic

        instructions = [
            models.Order(tid=1, price=Decimal('1.0000'), size=1),
            models.Order(tid=1, price=Decimal('2.0000'), size=2),
            models.Order(tid=2, price=Decimal('1.0000'), size=1),
            models.Order(tid=3, price=Decimal('1.0000'), size=1),
            models.Cancel(xtid=1),
            models.Cancel(xtid=2),
            models.CancelReplace(xr_tid=1, new_price=Decimal('10.0000'), new_size=10),
            models.CancelReplace(xr_tid=2, new_price=Decimal('20.0000'), new_size=20),
        ]
        result = logic.filter_by_oid(instructions, 1)
        assert len(result) == 4

        assert logic.filter_by_oid(instructions, 1) == logic.filter_by_oid_alt(instructions, 1)
