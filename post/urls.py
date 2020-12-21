from django.urls import path
from .views import MainView, PostJsonListView

app_name = 'posts'

urlpatterns = [
    path('list/', MainView.as_view(), name='main-view'),
    path('post-json/<int:num_posts>/', PostJsonListView.as_view(), name='posts-json-view'),
]
