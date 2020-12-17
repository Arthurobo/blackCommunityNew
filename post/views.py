# from django.shortcuts import render, redirect
# from django.urls import reverse_lazy
# from .models import Post, Like
# from account.models import Profile
# from django.views.generic import UpdateView, DeleteView
# from django.contrib import messages
# from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
# # Create your views here.

# @login_required
# def like_unlike_post(request):
#     user = request.user
#     if request.method == 'POST':
#         post_id = request.POST.get('post_id')
#         post_obj = Post.objects.get(id=post_id)
#         profile = Profile.objects.get(user=user)

#         if profile in post_obj.liked.all():
#             post_obj.liked.remove(profile)
#         else:
#             post_obj.liked.add(profile)

#         like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

#         if not created:
#             if like.value=='Like':
#                 like.value='Unlike'
#             else:
#                 like.value='Like'
#         else:
#             like.value='Like'

#             post_obj.save()
#             like.save()

#         # data = {
#         #     'value': like.value,
#         #     'likes': post_obj.liked.all().count()
#         # }

#         # return JsonResponse(data, safe=False)
#     return redirect('/')
