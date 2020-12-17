from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from account.forms import (RegistrationForm, AccountAuthenticationForm, 
                            AccountUpdateForm, ProfileImageUpdateForm, UserProfileUpdateForm)
from django.conf import settings
from account.models import Account, Profile
from page.models import Page
from post.models import Post
from django.forms.models import model_to_dict
from django.views.generic import View, CreateView
from django.utils.http import is_safe_url
from django.contrib.auth.decorators import login_required

from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
import os
import cv2
import json
import base64
import requests
from django.core import files
from friend.utils import get_friend_request_or_false
from friend.friend_request_status import FriendRequestStatus
from friend.models import FriendList, FriendRequest

TEMP_PROFILE_IMAGE_NAME = "temp_profile_image.png"


def register_view(request, *args, **kwargs):
    user = request.user

    if user.is_authenticated:
        return redirect("personal:home")

    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            # sex = form.cleaned_data.get('sex')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password,
                                    first_name=first_name, last_name=last_name)  # sex=sex
            login(request, account)
            destination = get_redirect_if_exists(request)
            if destination:
                return redirect(destination)
            return redirect("personal:home")
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('personal:home')


# Old view but to stay here for now

# def login_view(request, *args, **kwargs):
#     context = {}
#     user = request.user
#     if user.is_authenticated:
#         return redirect("personal:home")
#     destination = get_redirect_if_exists(request)

#     if request.POST:
#         form = AccountAuthenticationForm(request.POST)
#         if form.is_valid():
#             email = request.POST['email']
#             password = request.POST['password']
#             user = authenticate(email=email, password=password)

#             if user:
#                 login(request, user)
#                 if destination:
#                     return redirect(destination)
#                 return redirect("personal:home")
#     else:
#         form = AccountAuthenticationForm()
#     context['login_form'] = form
#     return render(request, "account/login.html", context)


# New login view that redirects and not like the old login 
# view that uses the get_redirect_f _exists
def login_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("personal:home")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                if request.GET:
                    if request.GET.get("next"):
                        return redirect(request.GET.get('next'))
                return redirect("personal:home")
    else:
        form = AccountAuthenticationForm()
    context['login_form'] = form
    return render(request, "account/login.html", context)


def get_redirect_if_exists(request):
    # redirect = None
    redirect = settings.LOGIN_REDIRECT_URL
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("NEXT"))
    return redirect


# def user_detail(request, username):
#     context = {}
#     user = get_object_or_404(Account, username=username, is_active=True)
    
#     context['user'] = user
#     return render(request, 'account/userDetail.html', context)

@login_required
def account_view(request, *args, **kwargs):
    context = {}
    user_id = kwargs.get("user_id")
    #page = Page.objects.filter(owner=request.user.profile)#.order_by('-cr_date')
    try:
        account = Account.objects.get(pk=user_id)
        profile = Profile.objects.get(pk=user_id)
        page = Page.objects.filter(owner=profile.user_id).order_by('-date_created')
        post = Post.objects.filter(author=profile.user_id)
    except:
        return HttpResponse('Something went wrong.')

    if request.method == "GET":
        context['id'] = account.id
        context['username'] = account.username
        context['first_name'] = account.first_name
        context['last_name'] = account.last_name
        context['email'] = account.email
        context['profile_image'] = account.profile_image.url
        context['hide_email'] = account.hide_email
        context['bio'] = profile.bio
        context['phone_number'] = profile.phone_number
        context['country_of_origin'] = profile.country_of_origin
        context['state_of_origin'] = profile.state_of_origin
        context['tribe'] = profile.tribe
        context['country_of_residence'] = profile.country_of_residence
        context['state_of_residence'] = profile.state_of_residence
        context['city_of_residence'] = profile.city_of_residence
        context['address_location'] = profile.address_location
        context['tribes_intrested_in'] = profile.tribes_intrested_in
        context['page'] = page
        context['post'] = post

        try:
            friend_list = FriendList.objects.get(user=account)
        except FriendList.DoesNotExist:
            friend_list = FriendList(user=account)
            friend_list.save()
        friends = friend_list.friends.all()
        context['friends'] = friends

        is_self = True
        is_friend = False
        request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
        friend_requests = None
        user = request.user
        if user.is_authenticated and user != account:
            is_self = False
            if friends.filter(pk=user.id):
                is_friend = True
            else:
                is_friend = False
                if get_friend_request_or_false(sender=account, receiver=user) != False:
                    request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
                    context['pending_friend_request_id'] = get_friend_request_or_false(sender=account, receiver=user).id
				# CASE2: Request has been sent from YOU to THEM: FriendRequestStatus.YOU_SENT_TO_THEM
                elif get_friend_request_or_false(sender=user, receiver=account) != False:
                    request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
				# CASE3: No request sent from YOU or THEM: FriendRequestStatus.NO_REQUEST_SENT
                else:
                    request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
        
        elif not user.is_authenticated:
            is_self = False
        else:
            try:
                friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
            except:
                pass
            # Set the template variables to the values
        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['request_sent'] = request_sent
        context['friend_requests'] = friend_requests
        context['BASE_URL'] = settings.BASE_URL
    


        return render(request, "account/account.html", context)

    
@login_required
def edit_account_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('login')
    user_id = kwargs.get("user_id")
    account = Account.objects.get(pk=user_id)
    if account.pk != request.user.pk:
        return HttpResponse("You cannot edit someone elses profile.")
    context = {}
    if request.POST:
        form = AccountUpdateForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            #new_username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            return redirect("account:user-account-view", user_id=account.pk)
        else:
            form = AccountUpdateForm(request.POST, instance=request.user,
                    initial={
                        "id": account.pk,
                        "email": account.email,
                        #"username": account.username,
                        "first_name": account.first_name,
                        "last_name": account.last_name,
                        "hide_email": account.hide_email,
                    })
            context['forom'] = form
    else:
        form = AccountUpdateForm(
			initial={
					"id": account.pk,
					"email": account.email,
					#"username": account.username,
					"first_name": account.first_name,
					"last_name": account.last_name,
					"hide_email": account.hide_email,
				}
			)
        context['form'] = form
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, 'account/edit_account.html', context)


@login_required
def save_temp_profile_image_from_base64String(imageString, user):
	INCORRECT_PADDING_EXCEPTION = "Incorrect padding"
	try:
		if not os.path.exists(settings.TEMP):
			os.mkdir(settings.TEMP)
		if not os.path.exists(settings.TEMP + "/" + str(user.pk)):
			os.mkdir(settings.TEMP + "/" + str(user.pk))
		url = os.path.join(settings.TEMP + "/" + str(user.pk),TEMP_PROFILE_IMAGE_NAME)
		storage = FileSystemStorage(location=url)
		image = base64.b64decode(imageString)
		with storage.open('', 'wb+') as destination:
			destination.write(image)
			destination.close()
		return url
	except Exception as e:
		print("exception: " + str(e))
		# workaround for an issue I found
		if str(e) == INCORRECT_PADDING_EXCEPTION:
			imageString += "=" * ((4 - len(imageString) % 4) % 4)
			return save_temp_profile_image_from_base64String(imageString, user)
	return None


@login_required
def crop_image(request, *args, **kwargs):
    payload = {}
    user = request.user
    if request.POST and user.is_authenticated:
        try:
            imageString = request.POST.get("image")
            url = save_temp_profile_image_from_base64String(imageString, user)
            img = cv2.imread(url)

            # cv2 resize function
            # src = cv2.imread(url, cv2.IMREAD_UNCHANGED)
            # scale_percent = 100
            # width = int(src.shape[1] * scale_percent / 100)
            # height = int(src.shape[0] * scale_percent / 100)
            # dsize = (width, height)
            # output = cv2.resize(src, dsize)
            # cv2.imwrite(url, output)
                        
            cropX = int(float(str(request.POST.get("cropX"))))
            cropY = int(float(str(request.POST.get("cropY"))))
            cropWidth = int(float(str(request.POST.get("cropWidth"))))
            cropHeight = int(float(str(request.POST.get("cropHeight"))))
            if cropX < 0:
                cropX = 0
            if cropY < 0: # There is a bug with cropperjs. y can be negative.
                cropY = 0
            crop_img = img[cropY:cropY+cropHeight, cropX:cropX+cropWidth]

            cv2.imwrite(url, crop_img)

            # delete the old image
            user.profile_image.delete()

            # Save the cropped image to user model
            user.profile_image.save("profile_image.png", files.File(open(url, 'rb')))
            user.save()

            payload['result'] = "success"
            payload['cropped_profile_image'] = user.profile_image.url

            # delete temp file
            os.remove(url)
			
        except Exception as e:
            print("exception: " + str(e))
            payload['result'] = "error"
            payload['exception'] = str(e)
    return HttpResponse(json.dumps(payload), content_type="application/json")


@login_required
def edit_profile_image_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('account:login')
    user_id = kwargs.get('user_id')
    account = Account.objects.get(pk=user_id)
    if account.pk != request.user.pk:
        return HttpResponse("You cannot edit someone elses profile Image.")
    context = {}
    if request.POST:
        form = ProfileImageUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # account.profile_image.delete()
            form.save()
            return redirect("account:user-account-view", user_id=account.pk)
        else:
            form = ProfileImageUpdateForm(request.POST, instance=request.user,
                initial = {
                    "id": account.pk,
                    "profile_image": account.profile_image,
                })
            context['form'] = form
    else:
        form = ProfileImageUpdateForm(
            initial={
                "id": account.pk,
                "profile_image": account.profile_image,
                }
            )
        context['form'] = form
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, "account/edit_profile_image.html", context)



@login_required
def edit_user_profile_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('account:login')
    user_id = kwargs.get('user_id')
    account = Account.objects.get(pk=user_id)
    profile = Profile.objects.get(pk=user_id)
    if account.pk != request.user.pk:
        return HttpResponse("You cannot edit someone elses profile credentials.")
    
    context = {}
    if request.POST:
        form = UserProfileUpdateForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            # account.profile_image.delete()
            form.save()
            return redirect("account:user-account-view", user_id=account.pk)
        else:
            form = UserProfileUpdateForm(request.POST, instance=request.user.profile,
                initial = {
                    "id": profile.pk,
                    "bio": profile.bio,
                    "phone_number": profile.phone_number,
                    'country_of_origin': profile.country_of_origin, 
                    'state_of_origin': profile.state_of_origin, 
                    'tribe': profile.tribe, 
                    'country_of_residence': profile.country_of_residence, 
                    'state_of_residence': profile.state_of_residence, 
                    'city_of_residence': profile.city_of_residence, 
                    'address_location': profile.address_location,
                    'tribes_intrested_in': profile.tribes_intrested_in,
                })
            context['form'] = form
    else:
        form = UserProfileUpdateForm(
            initial={
                    "id": profile.pk,
                    "bio": profile.bio,
                    "phone_number": profile.phone_number,
                    'country_of_origin': profile.country_of_origin, 
                    'state_of_origin': profile.state_of_origin, 
                    'tribe': profile.tribe, 
                    'country_of_residence': profile.country_of_residence, 
                    'state_of_residence': profile.state_of_residence, 
                    'city_of_residence': profile.city_of_residence, 
                    'address_location': profile.address_location,
                    'tribes_intrested_in': profile.tribes_intrested_in,
                }
            )
        context['form'] = form
    return render(request, "account/edit_profile.html", context)
