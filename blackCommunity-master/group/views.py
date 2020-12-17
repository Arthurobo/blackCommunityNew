from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Group, Post
from .forms import GroupCreateForm, GroupPostCreateForm
from django.urls import reverse_lazy, reverse
from account.models import Profile
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import FormMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# def group_list(request):
#     groups = Group.objects.all()
#     paginator = Paginator(groups, 6)
#     page = request.GET.get('page')

#     try:
#         images = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer deliver the first page
#         images = paginator.page(1)
#     except EmptyPage:
#         if request.is_ajax():
#             # If the request is AJAX and the page is out of range
#             # return an empty page
#             return HttpResponse('')
#         images = paginator.page(paginator.num_pages)
#     if request.is_ajax():
#         return render(request, "group/group_list_ajax.html", {'section': 'groups', 'groups': groups })
#     return render(request, "group/group_list.html", {'section': 'groups', 'groups': groups })


class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    paginate_by = 8
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
        total_likes = group.total_likes()
        context['total_likes'] = total_likes
        return context

def LikeView(request, pk):
    group = get_object_or_404(Group, id=request.POST.get('group_id'))
    group.likes.add(request.user.profile)
    return HttpResponseRedirect(reverse('group:group-detail-view', args=[str(pk)]))