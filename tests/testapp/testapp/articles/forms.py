from django import forms
from .models import AbstractRegionalArticle


class NewArticleForm(forms.ModelForm):
    class Meta:
        model = AbstractRegionalArticle
