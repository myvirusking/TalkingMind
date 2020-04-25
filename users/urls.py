from django.urls import path
from . import views
from users.views import HomeView
from django.contrib.auth.decorators import login_required
from blog import  views as blog_view
from .views import SelectFavouriteArticleCategoryView


urlpatterns = [
    path('registration/', views.user_register, name='registration-form'),
    path('home/', blog_view.home, name='login-home'),
    path('fav/article/category/',SelectFavouriteArticleCategoryView.as_view(), name='fav_article_category'),
]
