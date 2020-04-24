from django.urls import path
from .import views
from .views import  PostUpdateView,PostDeleteView
from blog.views import HomeView

urlpatterns = [
    path('talkingMind/', HomeView.as_view(), name='blog-home'),
    #path('about/', views.about, name="blog-about"),
    path('post/<int:pk>/update/',PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete')

]
