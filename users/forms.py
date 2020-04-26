from django import forms
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from .models import Profile
from blog.models import Post
import re


class RegisterForm(forms.ModelForm):

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control regInput', 'placeholder': 'Username', 'id': 'username'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control regInput', 'placeholder': 'Email', 'id': 'email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control regInput', 'placeholder': 'Password', 'id': 'pswrd'
    }))

    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control regInput', 'placeholder': 'Confirm password', 'id': 'repeatPswrd'
    }))

    def clean_username(self, *args, **kwargs):
        uname = self.cleaned_data.get("username")
        if re.match(r'^[A-Za-z0-9]+(?:[ _-][A-Za-z0-9]+)*$', uname) is not None:
            print("correct")
            return uname
        else:
            print("Error in username")
            raise forms.ValidationError("Enter valid username")

    class Meta:
        model = User
        fields = ['username','email','password','repeat_password',]

    # def clean_email(self, *args, **kwargs):
    #     email = self.cleaned_data.get("email")
    #     if re.match(r'^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,7}$',
    #                 email) is not None:
    #
    #         return email
    #     else:
    #         print(email)
    #         raise forms.ValidationError("Enter a valid email address")


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'validate form-control','placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password','class': 'form-control'}))


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(widget=TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    about = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','rows':'5'}))

    class Meta:
        model = Profile
        fields = ['about','image']


