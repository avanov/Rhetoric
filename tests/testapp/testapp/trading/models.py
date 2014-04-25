from django.db import models
from rhetoric.adt import adt


class Order(models.Model):
     tid = models.IntegerField(null=False)
     price = models.DecimalField(null=False, max_digits=16, decimal_places=4, default='0')
     size = models.IntegerField(null=False, default=0)


class Cancel(models.Model):
    xtid = models.IntegerField(null=False)


class CancelReplace(models.Model):
    xr_tid = models.IntegerField(null=False)
    new_price = models.DecimalField(null=False, max_digits=16, decimal_places=4, default='0')
    new_size = models.IntegerField(null=False, default=0)


class Instruction(adt):
    ORDER = Order
    CANCEL = Cancel
    CANCEL_REPLACE = CancelReplace
