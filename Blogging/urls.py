"""Blogging URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users.forms import (
    CustomAuthForm,
    CustomPasswordResetForm,
    CustomPasswordResetEmailForm)
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from blog import views as blog_views
from settings.forms import CustomPasswordChangeForm
from settings import views as setting_views
from django.contrib import messages


urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('user/', include('users.urls')),
    path('profile/',user_views.profile, name='profile'),
    path('login/', user_views.CustomLoginView.as_view(),name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/login.html', next_page='/login/'), name='logout'),
    path('other-profile/<int:pk>/', user_views.other_user_profile, name='other-profile'),
    path('user/follow-request/send/', user_views.send_follow_request ,name='send_follow_request'),
    path('user/follow-request/cancel/', user_views.cancel_follow_request ,name='cancel_follow_request'),
    path('user/follow-request/accept/', user_views.accept_follow_request ,name='accept_follow_request'),
    path('user/follow-request/delete/', user_views.delete_follow_request ,name='delete_follow_request'),
    path('user/other-profile/unfollow/', user_views.unfollow_user, name='unfollow_user'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name = 'users/password_reset.html', form_class = CustomPasswordResetEmailForm,
         ),
         name='password_reset'),
    path('password-rest/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'),
         name='password_reset_done'
         ),
   path('password-reset-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html', form_class=CustomPasswordResetForm,
         ),
         name='password_reset_confirm'),
    path('password-rest-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'),
             name='password_reset_complete'
         ),

    path('change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='settings/changePassword.html',
            form_class=CustomPasswordChangeForm,
        ),
        name='change_password'
    ),

    path('password-change-done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='settings/passwordChangeSuccess.html'
         ),
        name='password_change_done'
    ),

         # Search user
    path('userSearch/',user_views.user_search_view,name="user_search"),

    path('like/', blog_views.post_like, name="like-post"),

    path('save/', blog_views.save_post, name="save-post"),

    path('user/saved_post/', blog_views.SavedPostView.as_view(), name='saved-post-list'),

    path('post/<int:pid>/', blog_views.single_post, name="single-post"),

    path('post/<int:pid>/comment_like/', blog_views.comment_like, name="like-comment"),

    path('comment/', blog_views.comment, name="comment"),

    path('remove-from-followers/', user_views.remove_from_followers_list, name='remove-from-follower-list'),

    path('notification/', user_views.notification_view, name='notification'),

    path('new-notification/', blog_views.check_for_new_notification, name='new-notification'),

    path('profile-setting/', setting_views.change_profile_setting, name='profile-setting'),

    path('security-setting/', setting_views.security_setting, name='security-setting'),

    path('two-factor-auth-setting/', setting_views.two_factor_authentication, name='two-fact-auth-setting')

]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
