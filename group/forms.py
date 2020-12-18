from .models import Group, Post, Comment
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


class GroupPostCommentForm(forms.ModelForm):
    body = forms.CharField(label='',
                            widget=forms.TextInput(attrs={'placeholder': "Add a comment..."}))

    class Meta:
        model = Comment
        fields = ('body',)