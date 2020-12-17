from django.urls import path
from .views import (
                    register_view, logout_view, login_view, account_view, 
                    edit_account_view, edit_profile_image_view, crop_image, #user_detail
                    edit_user_profile_view
                    )

app_name = "account"

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('<user_id>/', account_view, name='user-account-view'),
    # path('users/<str:username>/', user_detail, name='user_detail'),
    path('<user_id>/edit/', edit_account_view, name='edit-account'),
    path('<user_id>/profile-image/edit/', edit_profile_image_view, name='edit-profile-image'),
	path('<user_id>/edit/crop_image/', crop_image, name="crop-image"),



    # Profile
    
    path('<user_id>/profile/update/', edit_user_profile_view, name='edit-user-profile-view'),
    
]