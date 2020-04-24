from django.urls import path
from . import views
from users.views import HomeView
from django.contrib.auth.decorators import login_required
from blog import  views as blog_view



urlpatterns = [
    path('registration/', views.user_register, name='registration-form'),
    path('home/', blog_view.home, name='login-home'),
]
