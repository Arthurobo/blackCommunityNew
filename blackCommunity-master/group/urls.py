from django.urls import path

from .views import GroupCreateView, GroupDetailView, GroupListView, LikeView #group_list

app_name = 'group'

urlpatterns = [
    path('list/', GroupListView.as_view(), name='group-list-view'),
    # path('list/', group_list, name='group-list-view'),
    path('create/', GroupCreateView.as_view(), name='group-create-view'),
    path('<int:pk>/', GroupDetailView.as_view(), name='group-detail-view'),
    path('like/<int:pk>/', LikeView, name='like-group'),
]