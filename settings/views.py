from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import AccountPrivacySetting
from users.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from users.forms import UserUpdateForm, ProfileUpdateForm, AboutForm
from two_factor.views import SetupView,QRGeneratorView,BackupTokensView
from .forms import CustomTOTPDeviceForm,CustomDeviceValidationForm,CustomePhoneNumberForm
from django.views.decorators.cache import never_cache
from django_otp.decorators import otp_required
from django.views.generic import TemplateView
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_static.models import StaticDevice
from two_factor.models import PhoneDevice
from django_otp import devices_for_user
import django_otp
from django_otp.oath import TOTP
from django_otp.util import random_hex
from axes.models import AccessAttempt
import Blogging.settings
from django.core.mail import send_mail
from django.conf import settings
from user_sessions.views import SessionDeleteView



def change_profile_privacy(request):
    profile_privacy = request.POST['profile_privacy']
    logged_in_user = User.objects.get(user=request.user)

    if profile_privacy == 'private':
        AccountPrivacySetting.objects.update(
                                            user=logged_in_user,
                                            profile_privacy=profile_privacy).save()
    elif profile_privacy == 'public':
        AccountPrivacySetting.objects.update(
                                            user=logged_in_user,
                                            profile_privacy=profile_privacy).save()


@login_required
def change_profile_setting(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        about_form = AboutForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        else:
            print("Invalid")

        if about_form.is_valid():
            about_form.save()

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        about_form = AboutForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'about_form': about_form
    }

    return render(request, 'settings/profileSetting.html', context)


@login_required
def security_setting(request):
        return render(request, 'settings/securitySetting.html')


"""
it will handle user devices like change device name,delete device etc,
whenever new device will be added or deleted.
"""
def userDevicesHandler(user,method,deviceModel=None):
    all_devices = list(devices_for_user(user))
    if method == "added" and len(all_devices) > 1:
        for device in all_devices:
            if isinstance(device,TOTPDevice):
                if device.name != "default":
                    device.name = "default"
                    device.save()
            elif isinstance(device,PhoneDevice):
                if device.name != "backup":
                    device.name = "backup"
                    device.save()
    elif method == "deleted":
        for device in all_devices:
            if isinstance(device,StaticDevice):
                if len(all_devices) == 2:
                    device.delete()
            elif isinstance(device,deviceModel):
                device.delete()
                all_devices.remove(device)
            elif isinstance(device,TOTPDevice) or isinstance(device,PhoneDevice):
                if device.name != "default":
                    device.name = "default"
                    device.save()


class TwoFactorAuthenticationProfile(TemplateView):
    template_name = 'settings/twoFactorAuthentication.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        for device in devices_for_user(request.user):
            if isinstance(device,TOTPDevice):
                context["device_generator"] = True
            elif isinstance(device,PhoneDevice):
                context["device_sms"] = True
        
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        method = request.POST['method']
        if method == 'enable_generator':
            return redirect('/setting/two-factor-auth/setup/?method=generator')
        elif method == 'enable_sms':
            return redirect('/setting/two-factor-auth/setup/?method=sms')
        elif method == 'disable_generator':
            userDevicesHandler(request.user,"deleted",TOTPDevice)
            return redirect('two-fact-auth-setting')
        elif method =='disable_sms':
            userDevicesHandler(request.user,"deleted",PhoneDevice)
            return redirect('two-fact-auth-setting')
        else:
            return redirect('two-fact-auth-setting')


class CustomTwoFactorAuthSetup(SetupView):
    qrcode_url = "2fa_qrcode"
    success_url = 'two-fact-auth-setting'
    session_key_name = "QR_KEY"
    template_name = 'settings/two_factor_auth_setup.html'
    form_list = (
        ('generator', CustomTOTPDeviceForm),
        ('sms', CustomePhoneNumberForm),
        ('validation', CustomDeviceValidationForm),    
    )

    def get(self, request, *args, **kwargs):
        devices_name = []
        for device in devices_for_user(self.request.user):
            if isinstance(device,PhoneDevice):
                devices_name.append("sms")
            elif isinstance(device,TOTPDevice):
                devices_name.append("generator")
        try:
            method = self.request.GET['method']
            if method == 'sms' and method not in devices_name:
                return self.render_goto_step('sms')
            elif method == 'generator' and method not in devices_name:
                return self.render_goto_step('generator')
            else:
                raise Exception("Invalid Method!")
        except Exception:
            return redirect(self.success_url)

    def get_method(self):
        method_data = self.storage.validated_step_data.get('method', {})
        method_data['method'] = self.request.GET.get('method',None)
        return method_data.get('method', None)
    
    def done(self, form_list, **kwargs):
        try:
            del self.request.session[self.session_key_name]
        except KeyError:
            pass
        # TOTPDeviceForm
        if self.get_method() == 'generator':
            form = [form for form in form_list if isinstance(form, CustomTOTPDeviceForm)][0]
            device = form.save()
        # PhoneNumberForm
        elif self.get_method() == 'sms':
            device = self.get_device()
            device.save()
        else:
            raise NotImplementedError("Unknown method '%s'" % self.get_method())

        userDevicesHandler(self.request.user,"added")
        django_otp.login(self.request, device)
        return redirect(self.success_url)

    def get_device(self, **kwargs):
        method = self.get_method()
        kwargs = kwargs or {}
        kwargs['name'] = 'default'
        kwargs['user'] = self.request.user

        if method == 'sms':
            kwargs['method'] = method
            kwargs['number'] = "+918789898789" #this number is used for sending a text message.
            return PhoneDevice(key=self.get_key(method), **kwargs)
 
    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        if self.steps.current == 'sms':
            context.update({'skippedSMS': True})
        return context


class CustomQRGeneratorView(QRGeneratorView):
    session_key_name = "QR_KEY"


class CustomBackupTokensView(BackupTokensView):
    template_name = "settings/two_factor_auth_bkup_tokens.html"
    success_url = "2fa_backup_tokens"
    number_of_tokens = 5
def two_factor_authentication(request):

    return render(request, 'settings/twoFactorAuthentication.html')


key = random_hex(20).encode()
totop_obj = TOTP(key, step=300)


def send_otp_for_email_verification(request):
    a = Blogging.settings.CURRENT_USER
    user = User.objects.get(username=Blogging.settings.CURRENT_USER)
    email = user.email

    if request.method == 'GET':
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        send_otp_mail(totop_obj.token(), ip,email, user)

    if request.method == 'POST':
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        otp = int(request.POST['otp'])

        username = Blogging.settings.CURRENT_USER
        print(username)
        is_verifed = totop_obj.verify(otp,tolerance=1)
        print(is_verifed)
        if is_verifed:
            AccessAttempt.objects.get(ip_address=ip, username=username).delete()
            return render(request,'settings/otp_success.html')

    return render(request, 'settings/otp_screen.html', context={'email':email})


def send_otp_mail(otp, ip, email, user):

    message = 'Hey {0} we recieved many unsuccessful login attempts from the IP address: {1}, so the TP has been blocked due to suspicion, so to unblock that IP  please verify youself by entering the below 6-digit OTP. OTP is {2} If it wasn\'t you then your account might be in danger secure your account by changing your password'.format(user.username,ip,otp)

    send_mail(subject='Account verification mail',message=message,from_email=settings.EMAIL_HOST_USER,recipient_list=[email], fail_silently=False)


class CustomSessionDeleteView(SessionDeleteView):
    def delete(self, request, *args, **kwargs):
        if kwargs['pk'] == request.session.session_key:
            logout(request)
            return redirect('login')
        return super(CustomSessionDeleteView, self).delete(request, *args, **kwargs)



































