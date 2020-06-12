from django.db import models
from users.models import Profile
from django.contrib.auth.models import User


class AccountPrivacySetting(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='accountprivacysetting', null=True)
    profile_privacy = models.CharField(default='public', max_length=20)
