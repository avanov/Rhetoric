from django import forms


class BlogPostForm(forms.Form):
    slug = forms.CharField(max_length=140, min_length=1)
