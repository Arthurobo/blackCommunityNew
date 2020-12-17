from django.urls import path

from .views import (
                    GroupCreateView, 
                    GroupDetailView, 
                    GroupListView, 
                    GroupFollowToggle,
                    GroupFollowAPIToggle,
                    GroupPostLikeToggle,
                    GroupPostLikeAPIToggle,
                    GroupPostDetailView
                    #group_list
                )

app_name = 'group'

urlpatterns = [
    path('list/', GroupListView.as_view(), name='group-list-view'),
    # path('list/', group_list, name='group-list-view'),
    path('create/', GroupCreateView.as_view(), name='group-create-view'),
    path('<int:pk>/', GroupDetailView.as_view(), name='group-detail-view'),

    # Group Follow
    path('<id>/follow/', GroupFollowToggle.as_view(), name='group-follow-toggle'),
    path('api/<id>/follow/', GroupFollowAPIToggle.as_view(), name='group-follow-api-toggle'),
    
    # Group Post Like
    path('post/<id>/like/', GroupPostLikeToggle.as_view(), name='group-post-like-toggle'),
    path('post/api/<id>/like/', GroupPostLikeAPIToggle.as_view(), name='group-post-like-api-toggle'),
    
    path('post/<int:pk>/', GroupPostDetailView.as_view(), name='group-post-detail-view'),
]