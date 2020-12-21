from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Post
from account.models import Profile
from django.views.generic import UpdateView, DeleteView, View, TemplateView
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class MainView(TemplateView):
    template_name = 'post/main.html'



class PostJsonListView(View):
    def get(self, *args, **kwargs):
        print(kwargs)
        upper = kwargs.get('num_posts')
        lower = upper - 3
        posts = list(Post.objects.values()[lower:upper])
        posts_size = len(Post.objects.all())
        max_size = True if upper >= posts_size else False
        return JsonResponse({'data': posts, 'max': max_size}, safe=True)