from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.forms import PasswordInput
from django.contrib.auth.forms import PasswordChangeForm


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Old Password',
                                                               'class':'form-control regInput'}))
    new_password1 = forms.CharField(widget=PasswordInput(attrs={'placeholder':'New Password',
                                                                'class':'form-control regInput'}))
    new_password2 = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Confirm new password',
                                                                'class':'form-control regInput'}))

