from django.shortcuts import render
from .models import AccountPrivacySetting
from users.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from users.forms import UserUpdateForm, ProfileUpdateForm, AboutForm


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
























