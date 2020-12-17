from .models import Group, Post
from django import forms



class GroupCreateForm(forms.ModelForm):
    title = forms.CharField(label='Title',)
    description = forms.CharField(label='Description',)

    class Meta:
        model = Group
        fields = ('title', 'description',)


class GroupPostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content',)