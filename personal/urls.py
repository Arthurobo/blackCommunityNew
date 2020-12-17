from django.urls import path
from .views import explore_page, home_screen_view #PageListView

app_name = 'personal'

urlpatterns = [
    #path('', PageListView.as_view(), name='home'),
    path('', home_screen_view, name='home'),
    path('i/explore/', explore_page, name='explore-view'),
]
