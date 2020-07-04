from django.db import models
from users.models import Profile
from django.contrib.auth.models import User
from django.utils import timezone


class AccountPrivacySetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='accountprivacysetting', null=True)
    profile_privacy = models.CharField(default='public', max_length=20)
    unrecognized_login_alert = models.CharField(default='enabled', max_length=20)


class AuthorizedLogin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ip_address = models.GenericIPAddressField()
    browser_family = models.CharField(max_length=50)
    os_family = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.browser_family} - {self.os_family}"
