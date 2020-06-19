from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.forms import PasswordInput
from django.contrib.auth.forms import PasswordChangeForm
from two_factor.forms import TOTPDeviceForm,DeviceValidationForm,PhoneNumberForm
from two_factor.utils import totp_digits


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=PasswordInput(attrs={'class':'pl-2 font-weight-bold form-control regInput '}))
    new_password1 = forms.CharField(widget=PasswordInput(attrs={'class':'pl-2 font-weight-bold form-control regInput'}))
    new_password2 = forms.CharField(widget=PasswordInput(attrs={'class':'pl-2 font-weight-bold form-control regInput'}))

class CustomTOTPDeviceForm(TOTPDeviceForm):
    token  = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder': 'Token','required':''}),min_value=-0,max_value=int('9' * totp_digits()))

class CustomDeviceValidationForm(DeviceValidationForm):
    token  = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder': 'Token','required':''}),min_value=-1,max_value=int('9' * totp_digits()))

class CustomePhoneNumberForm(PhoneNumberForm):
    number = forms.CharField(required=False)

    