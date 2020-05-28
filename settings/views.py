from django.shortcuts import render
from .models import AccountPrivacySetting
from users.models import Profile


def change_profile_privacy(request):
    profile_privacy = request.POST['profile_privacy']
    logged_in_user_profile = Profile.objects.get(user=request.user)

    if profile_privacy == 'private':
        AccountPrivacySetting.objects.update(
                                            profile=logged_in_user_profile,
                                            profile_privacy=profile_privacy).save()
    elif profile_privacy == 'public':
        AccountPrivacySetting.objects.update(
                                            profile=logged_in_user_profile,
                                            profile_privacy=profile_privacy).save()














