from django.contrib import admin
from .models import AccountPrivacySetting,AuthorizedLogin

admin.site.register(AccountPrivacySetting)
admin.site.register(AuthorizedLogin)
