from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .models import AccountPrivacySetting
from users.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from users.forms import UserUpdateForm, ProfileUpdateForm, AboutForm
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


def two_factor_authentication(request):

    return render(request, 'settings/twoFactorAuthentication.html')


key = random_hex(20).encode()
totop_obj = TOTP(key, step=300)


def send_otp_for_email_verification(request):
    a = Blogging.settings.CURRENT_USER
    print("ABC:",a)
    user = User.objects.get(username=Blogging.settings.CURRENT_USER)
    email = user.email

    if request.method == 'GET':
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
            print(ip)
        else:
            ip = request.META.get('REMOTE_ADDR')
            print(ip)

        send_otp_mail(totop_obj.token(), ip,email, user)

    if request.method == 'POST':
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
            print(ip)
        else:
            ip = request.META.get('REMOTE_ADDR')
            print(ip)
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



































