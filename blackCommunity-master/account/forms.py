from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import Account, Profile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=50, help_text="Required. Add a valid email address.")
    first_name = forms.CharField(label='First Name',)
    last_name = forms.CharField(label='Last Name',)

    class Meta:
        model = Account
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2',)

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % email)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('email', 'first_name', 'last_name', 'hide_email') #  'username',

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     try:
    #         account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
    #     except Account.DoesNotExist:
    #         return username
    #     raise forms.ValidationError('Username "%s" is already in use.' % username)

    def save(self, commit=True):
        account = super(AccountUpdateForm, self).save(commit=False)
        account.email = self.cleaned_data['email'].lower()
        #account.username = self.cleaned_data['username']
        account.first_name = self.cleaned_data['first_name']
        account.last_name = self.cleaned_data['last_name']
        account.hide_email = self.cleaned_data['hide_email']
        if commit:
            account.save()
        return account

class ProfileImageUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('profile_image',)

    def save(self, commit=True):
        account = super(ProfileImageUpdateForm, self).save(commit=False)
        account.profile_image = self.cleaned_data['profile_image']
        if commit:
            account.save()
        return account


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio','phone_number', 'country_of_origin', 
                  'state_of_origin', 'tribe', 'country_of_residence', 
                  'state_of_residence', 'city_of_residence', 'address_location','tribes_intrested_in',)

    # def save(self, commit=True):
    #     profile = super(UserBioUpdateForm, self).save(commit=False)
    #     profile.bio = self.cleaned_data['bio']
    #     if commit:
    #         profile.save()
    #     return profile


# class BookForm(forms.ModelForm):
#     class Meta:
#         model = Book
#         fields = ('title', 'publication_date', 'author', 'price', 'pages', 'book_type', )