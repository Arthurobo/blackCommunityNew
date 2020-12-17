from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from friend.models import FriendList

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def get_profile_image_filepath(self, filename):
    return 'profile_images/' + str(self.username) + "_" + "_" + str(self.pk) + '/profile_image.png'

def get_default_profile_image():
    return "defaultProfileImage/default.jpg"


MALE = "M"
FEMALE = "F"
SEX_CHOICE = (
    (MALE, "Male"),
    (FEMALE, "Female"),
)


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=50, unique=True)
    username = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, 
                                        null=True, blank=True, default=get_default_profile_image)
    #sex = models.CharField(max_length=1, choices=SEX_CHOICE)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    hide_email = models.BooleanField(default=True)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index('profile_images/' + str(self.pk) + "/"):]

 	# To be sure of admin permissions, NOTE: all admins have permissions
    def has_perm(self, perm, obj=None):
        return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True   


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=50, blank=True)
    country_of_origin = models.CharField(max_length=50, blank=True)
    state_of_origin = models.CharField(max_length=50, blank=True)
    tribe = models.CharField(max_length=50, blank=True)
    country_of_residence = models.CharField(max_length=50, blank=True)    
    state_of_residence = models.CharField(max_length=50, blank=True)    
    city_of_residence = models.CharField(max_length=50, blank=True)   
    address_location = models.CharField(max_length=50, blank=True)
    tribes_intrested_in = models.CharField(max_length=50, blank=True) # Users can chose their tribes of interests  
    ip_address = models.CharField(max_length=50, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return str(self.user)


def profile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)


post_save.connect(profile_receiver, sender=settings.AUTH_USER_MODEL)


@receiver(post_save, sender=Account)
def user_save(sender, instance, **kwargs):
    FriendList.objects.get_or_create(user=instance)