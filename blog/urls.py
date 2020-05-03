from django.urls import path
from .views import  PostUpdateView,PostDeleteView,PostCreateView,HomeView

urlpatterns = [
    path('talkingMind/', HomeView.as_view(), name='blog-home'),
    #path('about/', views.about, name="blog-about"),
    path('post/<int:pk>/update/',PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/create/', PostCreateView.as_view(), name='post-create'),
]
