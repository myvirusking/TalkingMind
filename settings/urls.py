from django.urls import path,include
from settings import views as setting_views

urlpatterns = [
    path('profile/', setting_views.change_profile_setting, name='profile-setting'),
    path('profile/mobile/verify/', setting_views.mobile_verify_otp, name='profile_mobile_verify'),
    path('security/', setting_views.security_setting, name='security-setting'),
    path('two-factor-auth/', setting_views.TwoFactorAuthenticationProfile.as_view(), name='two-fact-auth-setting'),
    path('two-factor-auth/setup/', setting_views.CustomTwoFactorAuthSetup.as_view(), name='2fa_setup'),
    path('two-factor-auth/setup/qrcode/', setting_views.CustomQRGeneratorView.as_view(), name='2fa_qrcode'),
    path('two-factor-auth/backup/tokens/', setting_views.CustomBackupTokensView.as_view(), name='2fa_backup_tokens'),
    path('authorized-logins/', setting_views.AuthorizedLogins.as_view(), name='authorized_devices'),
    path('authorized-logins/<int:pk>/delete/', setting_views.DeleteAuthorizedLogin, name='delete_authorized_device'),
    path('sessions/', include('settings.user_sessions_url')),
]