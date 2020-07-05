from django import forms
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from .models import Profile
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth import password_validation
from blog.models import Post
import re
from two_factor.forms import AuthenticationTokenForm
from two_factor.utils import totp_digits
from two_factor.validators import validate_international_phonenumber

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control regInput mr-1 mb-0', 'placeholder': 'First name', 'id': 'fname'
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control regInput ml-1 mb-0', 'placeholder': 'Last name', 'id':'lname'
    }))

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control regInput', 'placeholder': 'Username', 'id': 'username'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control regInput', 'placeholder': 'Email', 'id': 'email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control regInput', 'placeholder': 'Password', 'id': 'pswrd'
    }),help_text=password_validation.password_validators_help_text_html())

    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control regInput', 'placeholder': 'Confirm password', 'id': 'repeatPswrd'
    }))

    def clean_username(self, *args, **kwargs):
        uname = self.cleaned_data.get("username")
        if re.match(r'^(?!.*[_\s-]{2,})[a-zA-Z][a-zA-Z0-9_\s\-]*[a-zA-Z0-9]$', uname) is None:
            raise forms.ValidationError("Username must not start with digit and also it must not start or end with any special characters")
        else:
            return uname

    def clean_password(self,*args, **kwargs):
        password_validation.validate_password(self.cleaned_data.get('password'), None)
        return self.cleaned_data.get('password')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'repeat_password',]



class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'validate form-control regInput','placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password','class': 'form-control regInput'}))


class CustomAuthenticationTokenForm(AuthenticationTokenForm):
    otp_token = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder': 'Confirmation Code'}),min_value=1,max_value=int('9' * totp_digits()))
    
    otp_error_messages = {
        'token_required': ('Please enter confirmation code.'),
        'invalid_token': ('Invalid code, please make sure you have entered it correctly.')
    }

class CustomBackupTokenForm(AuthenticationTokenForm):
    otp_token = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Backup Code','required':''}))

    otp_error_messages = {
        'token_required': ('Please enter backup code.'),
        'invalid_token': ('Invalid backup code, please make sure you have entered it correctly.')
    }

class CustomPasswordResetForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=PasswordInput(attrs={'placeholder':'New Password', 'class':'form-control regInput'}))
    new_password2 = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Confirm password', 'class':'form-control regInput'}))


class CustomPasswordResetEmailForm(PasswordResetForm):
    email = forms.EmailField(widget=TextInput(attrs={'class':'form-control regInput', 'placeholder':'Enter email'}))


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'pl-2', 'placeholder':'e.g. Elliot'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'pl-2', 'placeholder':'e.g. Alderson'}))
    email = forms.EmailField(widget=TextInput(attrs={'class':'pl-2', 'placeholder':'e.g. elliot@gmail.com',
                                                     'aria-describedby':'emailHelp'}))
    username = forms.CharField(widget=TextInput(attrs={'class':'pl-2', 'placeholder':'e.g. elliot_alderson'}))

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={'class':' pl-2','rows':'3',
                                                       'placeholder':'e.g. Blogger | Traveller | Optimist | Programmer'}))
    class Meta:
        model = Profile
        fields = [ 'bio','image','facebook','twitter', 'instagram']


class MobileNoUpdateForm(forms.ModelForm):
    mobile_no = forms.CharField(widget=TextInput(attrs={'class':'pl-2', 'aria-describedby':'phoneHelp',
                                                        }), required=False,validators=[validate_international_phonenumber])
    class Meta:
        model = Profile
        fields = ['mobile_no']

class AboutForm(forms.ModelForm):
    about = forms.CharField(widget=forms.Textarea(attrs={'class': 'pl-2', 'rows': '5',
                                                         'placeholder':'e.g. I am a blogger and I love to explore the beautiful places and enjoy each and every moment at fullest...'}))

    class Meta:
        model = Profile
        fields = ['about',]



