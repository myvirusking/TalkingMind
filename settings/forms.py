from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.forms import PasswordInput
from django.contrib.auth.forms import PasswordChangeForm
from two_factor.forms import TOTPDeviceForm,DeviceValidationForm,PhoneNumberForm
from two_factor.utils import totp_digits
from two_factor.validators import validate_international_phonenumber
from django.contrib.auth.models import User


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=PasswordInput(attrs={'class':'pl-2 font-weight-bold form-control regInput '}))
    new_password1 = forms.CharField(widget=PasswordInput(attrs={'class':'pl-2 font-weight-bold form-control regInput'}))
    new_password2 = forms.CharField(widget=PasswordInput(attrs={'class':'pl-2 font-weight-bold form-control regInput'}))

class CustomTOTPDeviceForm(TOTPDeviceForm):
    token  = forms.IntegerField(widget=forms.NumberInput(attrs={'style':'width:75%','class':'form-control','placeholder': 'Confirmation Code','required':''}),min_value=-0,max_value=int('9' * totp_digits()))
    
    error_messages = {
        'invalid_token': ('Entered code is not valid.')
    }

class CustomDeviceValidationForm(DeviceValidationForm):
    token  = forms.IntegerField(widget=forms.NumberInput(attrs={'style':'width:75%','class':'form-control','placeholder': 'Confirmation Code','required':''}),min_value=-1,max_value=int('9' * totp_digits()))
    
    error_messages = {
        'invalid_token': ('Entered code is not valid.')
    }

class CustomPhoneNumberForm(PhoneNumberForm):
    number = forms.CharField(required=False,widget=forms.TextInput(attrs={'style':'width:75%','class':'form-control','placeholder': 'Mobile Number'}),validators=[validate_international_phonenumber])

class PasswordConfirmationForm(forms.Form):
    password = forms.CharField(required=True,widget=PasswordInput(attrs={'style':'width:75%','placeholder':'Password', 'class':'form-control regInput'}))

    def __init__(self, user, **args):
        super().__init__(**args)
        self.user = user

    def clean_password(self):
        password = self.cleaned_data['password']
        if not self.user.check_password(password):
            raise forms.ValidationError("Please enter a correct password.")
        return password
    