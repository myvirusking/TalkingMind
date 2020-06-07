from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from settings.models import AccountPrivacySetting


@receiver(post_save,sender=User)
def create_profile(sender, instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save,sender=User)
def save_profile(sender, instance,**kwargs):
    instance.profile.save()


@receiver(post_save, sender=Profile)
def create_account_privacy_settings(sender, instance, created, **kwargs):
    if created:
        AccountPrivacySetting.objects.create(profile=instance)


@receiver(post_save, sender=Profile)
def save_account_privacy_settings(sender, instance, **kwargs):
    instance.accountprivacysetting.save()





