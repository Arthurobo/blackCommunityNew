from .models import Page, Post
from django import forms



class PageCreateForm(forms.ModelForm):
    title = forms.CharField(label='Title',)
    description = forms.CharField(label='Description',)

    class Meta:
        model = Page
        fields = ('title', 'description',)


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content',)