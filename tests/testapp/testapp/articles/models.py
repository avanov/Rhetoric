from django.db import models

from ..types import Language


class AbstractRegionalArticle(models.Model):
    title = models.CharField(max_length=250, null=False, default='')
    text = models.TextField(null=False, default='')

    class Meta:
        abstract = True


@Language.ENGLISH('store:articles')
class EnglishArticle(AbstractRegionalArticle):
    pass

@Language.GERMAN('store:articles')
class GermanArticle(AbstractRegionalArticle):
    pass
