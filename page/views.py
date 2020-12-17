from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Page, Post
from .forms import PostCreateForm
from django.urls import reverse_lazy, reverse
from account.models import Profile
from django.http import HttpResponse
from django.views.generic.edit import FormMixin

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

class PageListView(ListView):
    model = Page
    template_name = 'page/page_list.html'

class PageCreateView(LoginRequiredMixin, CreateView):
    model = Page
    fields = ['title', 'description']
    template_name = 'page/page_create.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        return super().form_valid(form)


class PageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Page
    fields = ['title', 'description']
    template_name = 'page/page_update.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        return super().form_valid(form)

    def test_func(self):
        page = self.get_object()
        return page.owner == self.request.user.profile
        if self.request.user == page.owner:
            return True
        return False


class PageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Page
    success_url = '/'
    template_name = 'page/page_confirm_delete.html'

    def test_func(self):
        page = self.get_object()
        return page.owner == self.request.user.profile
        if self.request.user == page.owner:
            return True
        return False
        

class PageDetailView(FormMixin, DetailView):
    model = Page
    template_name = 'page/page_detail.html'
    form_class = PostCreateForm

    def get_success_url(self):
        return reverse('page:page-detail-view', kwargs={'slug': self.object.slug}) 

    def post(self, request, slug):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            messages.success(request, "New post added successfully")
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.page = self.object
        form.instance.author = self.request.user.profile
        if form.instance.author and self.request.user.profile == form.instance.page.owner:
            form.save()
        else:
            return HttpResponse("Create your own page so you can post, lol")
        return super(PageDetailView, self).form_valid(form)

class PageLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        obj = get_object_or_404(Page, slug=slug)
        url_ = obj.get_absolute_url()
        user = self.request.user.profile
        if self.request.user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
            return url_

class PageLikeAPIToggle(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, slug=None, format=None):
        obj = get_object_or_404(Page, slug=slug)
        url_ = obj.get_absolute_url()
        user = self.request.user.profile
        updated = False
        liked = False
        if self.request.user.is_authenticated:
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
            else:
                liked = True
                obj.likes.add(user)
            updated = True
        counts = obj.likes.count()
        data = {
            "updated": updated,
            "liked": liked,
            "likescount": counts
        }
        return Response(data)


class PagePostLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        id_ = self.kwargs.get("id")
        obj = get_object_or_404(Post, id=id_)
        url_ = obj.get_absolute_url()
        user = self.request.user.profile
        if self.request.user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.ad(user)
        return url_

    
class PagePostLikeAPIToggle(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, id=None, format=None):
        obj = get_object_or_404(Post, id=id)
        url_ = obj.get_absolute_url()
        user = self.request.user.profile
        updated = False
        liked = False
        if self.request.user.is_authenticated:
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
            else:
                liked = True
                obj.likes.add(user)
            updated = True
        likescount = obj.likes.count()
        data = {
            "updated": updated,
            "liked": liked,
            "likescount": likescount,
        }
        return Response(data)


class PagePostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "page/post_detail.html"