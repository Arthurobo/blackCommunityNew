from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Group, Post, Comment
from .forms import GroupCreateForm, GroupPostCreateForm, GroupPostCommentForm
from django.urls import reverse_lazy, reverse
from account.models import Profile
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import FormMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions


class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    paginate_by = 10
    context_object_name = 'groups'
    template_name = 'group/group_list.html'
    ordering = ['-date_created']


class GroupCreateView(LoginRequiredMixin, CreateView):
    model = Group
    fields = ['name', 'description']
    template_name = 'group/group_create.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        return super().form_valid(form)

class GroupDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Group
    template_name = 'group/group_detail.html'
    form_class = GroupPostCreateForm
    second_form_class = GroupPostCommentForm

    def get_success_url(self):
        return reverse('group:group-detail-view', kwargs={'pk': self.object.pk}) 

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            messages.success(request, "New post added successfully")
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
            
    def form_valid(self, form):
        form.instance.group = self.object
        form.instance.author = self.request.user.profile
        form.save()
        return super(GroupDetailView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(GroupDetailView, self).get_context_data()
        group = get_object_or_404(Group, id=self.kwargs['pk'])
        return context
    
    # def get_context_data(self, request, *args, **kwargs):
    #     context = super(GroupDetailView, self).get_context_data()
    #     _list = Post.objects.all()
    #     paginator = Paginator(_list, 5)
    #     page = request.GET.get('page')
    #     context['posts'] = paginator.get_page(page)
    #     group = get_object_or_404(Group, id=self.kwargs['pk'])
        
    #     return context




class GroupFollowToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        id_ = self.kwargs.get("id")
        obj = get_object_or_404(Group, id=id_)
        url_ = obj.get_absolute_url()
        user = self.request.user.profile
        if self.request.user.is_authenticated:
            if user in obj.follows.all():
                obj.follows.remove(user)
            else:
                obj.follows.add(user)
        return url_


class GroupFollowAPIToggle(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, id=None, format=None):
        obj = get_object_or_404(Group, id=id)
        url_ = obj.get_absolute_url()
        user = self.request.user.profile
        updated = False
        followed = False
        if self.request.user.is_authenticated:
            if user in obj.follows.all():
                followed = False
                obj.follows.remove(user)
            else:
                followed = True
                obj.follows.add(user)
            updated = True
        counts = obj.follows.count()
        data = {
            "updated": updated,
            "followed": followed,
            "followscount": counts
        }
        return Response(data)


class GroupPostLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        id_ = self.kwargs.get("id")
        obj = get_object_or_404(Post, id=id_)
        url_ = obj.get_absolute_url()
        user = self.request.user.profile
        if self.request.user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_


class GroupPostLikeAPIToggle(APIView):
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
        counts = obj.likes.count()
        data = {
            "updated": updated,
            "liked": liked,
            "likescount": counts
        }
        return Response(data)


class GroupPostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'group/post_detail.html'


class GroupPostCommentLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        id_ = self.kwargs.get("id")
        obj = get_object_or_404(Comment, id=id_)
        url_ = obj.get_absolute_url()
        user = self.request.user.profile
        if self.request.user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_


class GroupPostCommentLikeAPIToggle(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, id=None, format=None):
        obj = get_object_or_404(Comment, id=id)
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


class GroupPostCommentDetailView(LoginRequiredMixin, DetailView):
    model = Comment
    template_name = 'group/post_comment_detail.html'