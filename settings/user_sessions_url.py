from django.urls import path
from user_sessions.views import SessionDeleteOtherView, SessionListView
from .views import CustomSessionDeleteView

app_name = 'user_sessions'
urlpatterns = [
    path("active/",SessionListView.as_view(),name='session_list'),
    path("other/delete/",SessionDeleteOtherView.as_view(),name='session_delete_other'),
    path("<str:pk>/delete/",CustomSessionDeleteView.as_view(),name='session_delete')
]