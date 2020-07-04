from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import AccountPrivacySetting,AuthorizedLogin
from users.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from users.forms import UserUpdateForm, ProfileUpdateForm, AboutForm,MobileNoUpdateForm
from two_factor.views import SetupView,QRGeneratorView
from .forms import CustomTOTPDeviceForm,CustomDeviceValidationForm,CustomPhoneNumberForm,PasswordConfirmationForm
from django.views.decorators.cache import never_cache
from django_otp.decorators import otp_required
from django.views.generic import TemplateView,FormView,ListView
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_static.models import StaticDevice,StaticToken
from two_factor.models import PhoneDevice
from django_otp import devices_for_user
from django.contrib.auth.mixins import LoginRequiredMixin
import django_otp
from django.views.decorators.cache import never_cache
from two_factor.views.core import class_view_decorator
from django_otp.oath import TOTP
from django_otp.util import random_hex
from django.http import JsonResponse
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.forms import Form
from django.http import JsonResponse
from axes.models import AccessAttempt
import Blogging.settings
from django.core.mail import send_mail
from django.conf import settings
from user_sessions.views import SessionDeleteView
from user_sessions.models import Session
from django.db.models import Q

#Global generate otp object
totp_obj = TOTP(random_hex(20).encode(),step=300)

def mobile_send_otp(resend):
    if resend:
        global totp_obj
        totp_obj = TOTP(random_hex(20).encode(),step=600)
    print("Your OTP is:",totp_obj.token(),"\nvalid for 10 minutes only.")

def mobile_verify_otp(request):
    if request.method == "POST":
        resend_otp = request.POST.get('resend_otp',None)
        if resend_otp:
            mobile_send_otp(True)
            return JsonResponse({'success':'resent successfully'})
        else:
            global totp_obj
            otp = int(request.POST['otp'])
            new_number = request.POST['new_number']
            is_verify = totp_obj.verify(otp,tolerance=1)
            if is_verify:
                user_profile = request.user.profile
                user_profile.mobile_no = new_number
                user_profile.save()
                totp_obj = TOTP(random_hex(20).encode(),step=300)
            response = {'is_verify':is_verify}
            return JsonResponse(response)
    else:
        return redirect("profile-setting")


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

#image compression method
def compress(uncompressed_image):
    pil_image = Image.open(uncompressed_image)
    pil_image = pil_image.convert("RGB")
    image_io = BytesIO() 
    pil_image.save(image_io, 'JPEG', quality=75) 
    compressed_image = File(image_io, name=uncompressed_image.name)
    return compressed_image

@login_required
def change_profile_setting(request):
    if request.method == 'POST':
        if request.FILES:
            image = request.FILES['image']
            user_profile = request.user.profile
            user_profile.image.delete(False)
            user_profile.image = compress(image)
            user_profile.save()
            return redirect('profile-setting')
        else:
            old_mobile_no = request.user.profile.mobile_no
            user_form = UserUpdateForm(request.POST, instance=request.user)
            profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            about_form = AboutForm(request.POST, instance=request.user.profile)
            mobile_form = MobileNoUpdateForm(request.POST, instance=request.user.profile)
            
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
            else:
                print("Invalid")

            if about_form.is_valid():
                about_form.save()

            if mobile_form.is_valid():            
                new_mobile_no = mobile_form.cleaned_data['mobile_no']

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        about_form = AboutForm(instance=request.user.profile)
        mobile_form = MobileNoUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'about_form': about_form,
        'mobile_form' : mobile_form,
        'verify_mobile' : False
    }

    if mobile_form.is_valid() and user_form.is_valid() and new_mobile_no and old_mobile_no != new_mobile_no:
        context['verify_mobile'] = True
        context['new_mobile_no'] = new_mobile_no
        mobile_send_otp(False)

    return render(request, 'settings/profileSetting.html', context)


@login_required
def security_setting(request):
        return render(request, 'settings/securitySetting.html')


"""
it will handle user 2FA devices like changing device name,deleting device etc,
whenever new device will be added or deleted.
"""
def user2FADevicesHandler(user,method,deviceModel=None):
    all_devices = list(devices_for_user(user))
    devices_count = len(all_devices)
    if method == "added" and devices_count > 1:
        for device in all_devices:
            if isinstance(device,PhoneDevice):
                if device.name != "backup":
                    device.name = "backup"
                    device.save()
    elif method == "deleted":
        for device in all_devices:
            if isinstance(device,deviceModel):
                device.delete()
                devices_count -= 1
            elif isinstance(device,StaticDevice):
                if devices_count == 1:
                    device.delete()
            elif isinstance(device,PhoneDevice):
                if device.name != "default":
                    device.name = "default"
                    device.save()


class TwoFactorAuthenticationProfile(LoginRequiredMixin,FormView):
    template_name = 'settings/twoFactorAuthentication.html'
    form_class = PasswordConfirmationForm
    success_url = 'two-fact-auth-setting'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
                'user': self.request.user,
            })
        return kwargs

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        for device in devices_for_user(request.user):
            if isinstance(device,TOTPDevice):
                context["device_generator"] = True
            elif isinstance(device,PhoneDevice):
                context["device_sms"] = True
        
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        method = request.POST.get('method',None)
        if request.is_ajax():
            form = self.get_form()
            if form.is_valid():
                if method == 'disable_generator':
                    user2FADevicesHandler(request.user,"deleted",TOTPDevice)
                elif method =='disable_sms':
                    user2FADevicesHandler(request.user,"deleted",PhoneDevice)
                return JsonResponse({"is_verify":True})
            else:
                return JsonResponse({"is_verify":False})
        else:
            if method == 'enable_generator':
                return redirect('/setting/two-factor-auth/setup/?method=generator')
            elif method == 'enable_sms':
                return redirect('/setting/two-factor-auth/setup/?method=sms')
            else:
                return redirect('two-fact-auth-setting')


class CustomTwoFactorAuthSetup(SetupView):
    user_profile = None #It's used for fetching and updating user mobile number.
    qrcode_url = "2fa_qrcode"
    success_url = 'two-fact-auth-setting'
    session_key_name = "QR_KEY"
    template_name = 'settings/two_factor_auth_setup.html'
    form_list = (
        ('welcome', Form),
        ('verify_password', PasswordConfirmationForm),
        ('generator', CustomTOTPDeviceForm),
        ('sms', CustomPhoneNumberForm),
        ('validation', CustomDeviceValidationForm),
    )

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        if step == 'verify_password':
            kwargs.update({
                'user': self.request.user,
            })
        return kwargs

    def get(self, request, *args, **kwargs):
        devices_name = []
        for device in devices_for_user(self.request.user):
            if isinstance(device,PhoneDevice):
                devices_name.append("sms")
            elif isinstance(device,TOTPDevice):
                devices_name.append("generator")
        method = self.request.GET.get('method',None)
        if method == "sms" or method == "generator":#accept only method sms or generator
            if method in devices_name:
                return redirect(self.success_url)
        else:
            return redirect(self.success_url)
        return self.render_goto_step("welcome")

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
            if not self.user_profile.mobile_no:
                self.user_profile.mobile_no = self.storage.validated_step_data.get('sms', {}).get('number')
                self.user_profile.save()
            device = self.get_device()
            device.save()
        else:
            raise NotImplementedError("Unknown method '%s'" % self.get_method())

        user2FADevicesHandler(self.request.user,"added")
        django_otp.login(self.request, device)
        if self.request.user.staticdevice_set.all():
            return redirect(self.success_url)
        else:
            device = self.request.user.staticdevice_set.get_or_create(name='backup')[0]
            for n in range(5):
                device.token_set.create(token=StaticToken.random_token())
            return redirect("2fa_backup_tokens")

    def get_device(self, **kwargs):
        method = self.get_method()
        kwargs = kwargs or {}
        kwargs['name'] = 'default'
        kwargs['user'] = self.request.user

        if self.user_profile is None:
            self.user_profile =  Profile.objects.get(user=self.request.user)

        if method == 'sms':
            kwargs['method'] = method
            if self.user_profile and self.user_profile.mobile_no:
                kwargs['number'] = self.user_profile.mobile_no
            else:
                kwargs['number'] = self.storage.validated_step_data.get(method, {}).get('number')
            return PhoneDevice(key=self.get_key(method), **kwargs)
 
    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        if self.user_profile is None and self.steps.current == 'sms':
            self.user_profile =  Profile.objects.get(user=self.request.user)
        if self.steps.current == 'sms' and self.user_profile.mobile_no:
            context.update({'skipMobileForm': True})
        else:
            context.update({'skipMobileForm': False})
        return context


class CustomQRGeneratorView(QRGeneratorView):
    session_key_name = "QR_KEY"


@class_view_decorator(never_cache)
class CustomBackupTokensView(LoginRequiredMixin,TemplateView):
    template_name = "settings/two_factor_auth_bkup_tokens.html"
    success_url = "2fa_backup_tokens"
    number_of_tokens = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['device'] = self.get_device()
        return context

    def get_device(self):
        return self.request.user.staticdevice_set.get_or_create(name='backup')[0]

    def post(self, request, *args, **kwargs):
        device = self.get_device()
        device.token_set.all().delete()
        for n in range(self.number_of_tokens):
            device.token_set.create(token=StaticToken.random_token())
        return redirect(self.success_url)

    def get(self, request, *args, **kwargs):
        if list(devices_for_user(request.user)):
            return super().get(request, *args, **kwargs)
        else:
            return redirect("two-fact-auth-setting")


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


class AuthorizedLogins(LoginRequiredMixin,ListView):
    template_name = "settings/authorized_logins.html"
    ordering = '-created_at'
    context_object_name = "authorized_devices"

    def get_queryset(self):
        queryset = AuthorizedLogin.objects.filter(user=self.request.user)
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        self.queryset = queryset
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        browser_family = self.request.user_agent.browser.family
        os_family = self.request.user_agent.os.family
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        if self.queryset:
            current_device_obj = self.queryset.filter(browser_family=browser_family,os_family=os_family,ip_address=ip).first()
            kwargs["current_device_id"] = current_device_obj.id
        return super().get_context_data(**kwargs)


@login_required
def DeleteAuthorizedLogin(request,pk):
    authorized_device_obj = get_object_or_404(AuthorizedLogin,id=pk)
    session_obj = Session.objects.filter(Q(user = request.user) &
                                         Q(ip__exact = authorized_device_obj.ip_address) &
                                         Q(user_agent__icontains = authorized_device_obj.browser_family) &
                                         Q(user_agent__icontains = authorized_device_obj.os_family))
    if authorized_device_obj.user == request.user:
        if session_obj:
            session_obj.first().delete()
        authorized_device_obj.delete()
    return redirect("authorized_devices")






