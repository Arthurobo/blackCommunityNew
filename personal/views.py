from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.conf import settings

DEBUG = False

from page.models import Page #Article

# class PageListView(ListView):
#     model = Page
#     template_name = 'personal/home.html'

def home_screen_view(request, *args, **kwargs):
    context = {}
    context['debug_mode'] = settings.DEBUG
    context['debug'] = DEBUG
    context['room_id'] = "1"
    return render(request, 'personal/home.html', context)


def explore_page(request, *args, **kwargs):
    context = {}
    return render(request, 'personal/explore.html', context)