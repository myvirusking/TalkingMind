from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.forms import PasswordInput
from django.contrib.auth.forms import PasswordChangeForm


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=PasswordInput(attrs={'class':'pl-2 font-weight-bold form-control regInput '}))
    new_password1 = forms.CharField(widget=PasswordInput(attrs={'class':'pl-2 font-weight-bold form-control regInput'}))
    new_password2 = forms.CharField(widget=PasswordInput(attrs={'class':'pl-2 font-weight-bold form-control regInput'}))

