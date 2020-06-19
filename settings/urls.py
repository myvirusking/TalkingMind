from django.urls import path
from settings import views as setting_views

urlpatterns = [
    path('profile/', setting_views.change_profile_setting, name='profile-setting'),
    path('security/', setting_views.security_setting, name='security-setting'),
    path('two-factor-auth/', setting_views.TwoFactorAuthenticationProfile.as_view(), name='two-fact-auth-setting'),
    path('two-factor-auth/setup/', setting_views.CustomTwoFactorAuthSetup.as_view(), name='2fa_setup'),
    path('two-factor-auth/setup/qrcode/', setting_views.CustomQRGeneratorView.as_view(), name='2fa_qrcode'),
    path('two-factor-auth/backup/tokens/', setting_views.CustomBackupTokensView.as_view(), name='2fa_backup_tokens'),
]