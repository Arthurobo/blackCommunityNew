from django.urls import path

from .views import (
                    PageDetailView, 
                    PageCreateView, 
                    PageUpdateView, 
                    PageDeleteView, 
                    PageListView, 
                    PageLikeAPIToggle, 
                    PageLikeToggle,
                    PagePostLikeToggle,
                    PagePostLikeAPIToggle,
                    PagePostDetailView,
                )

app_name = 'page'

urlpatterns = [
    path('pages/list/', PageListView.as_view(), name='page-list'),
    path('<slug:slug>/', PageDetailView.as_view(), name='page-detail-view'),
    path('page/create/', PageCreateView.as_view(), name='page-create-view'),
    path('<slug:slug>/update/', PageUpdateView.as_view(), name='page-update-view'),
    path('<slug:slug>/delete/', PageDeleteView.as_view(), name='page-delete-view'),

    # Page LIke
    path('<slug>/like/', PageLikeToggle.as_view(), name='page-like-toggle'),
    path('api/<slug>/like/', PageLikeAPIToggle.as_view(), name='page-like-api-toggle'),

    # Page Post Like
    path('post/<id>/like/', PagePostLikeToggle.as_view(), name='page-post-like-toggle'),
    path('post/api/<id>/like/', PagePostLikeAPIToggle.as_view(), name='page-post-like-api-toggle'),
    
    path('post/<int:pk>/', PagePostDetailView.as_view(), name='page-post-detail-view'),
]