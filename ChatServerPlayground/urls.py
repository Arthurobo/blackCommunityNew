"""ChatServerPlayground URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
#from account.views import account_search_view

urlpatterns = [
    path('account/', include('account.urls', namespace='account')),
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls', namespace='chat')),
    path('friend/', include('friend.urls', namespace='friend')),
    path('', include('personal.urls', namespace='personal')),
    path('', include('page.urls', namespace='page')),
    path('group/', include('group.urls', namespace='group')),
    path('post/', include('post.urls', namespace='post')),
    # Search View
#    path('search/', account_search_view, name="search"),


    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('auth/password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name=
    'password_reset/password_change_done.html'), name='password_change_done'),

    path('auth/password_change/', auth_views.PasswordChangeView.as_view(template_name=
    'password_reset/password_change.html'), name='password_change'),

    path('auth/password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name=
    'password_reset/password_reset_done.html'), name='password_reset_done'),

    path('auth/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), 
    name='password_reset_confirm'),
    
    path('auth/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
    path('auth/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name=
    'password_reset/password_reset_complete.html'), name='password_reset_complete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)