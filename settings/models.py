from django.db import models
from users.models import Profile

class AccountPrivacySetting(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='accountprivacysetting', null=True)
    profile_privacy = models.CharField(default='public', max_length=20)
