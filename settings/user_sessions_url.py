from django.conf.urls import url
from user_sessions.views import SessionDeleteOtherView, SessionListView

from .views import CustomSessionDeleteView

app_name = 'user_sessions'
urlpatterns = [
    url(
        regex=r'^account/sessions/$',
        view=SessionListView.as_view(),
        name='session_list',
    ),
    url(
        regex=r'^account/sessions/other/delete/$',
        view=SessionDeleteOtherView.as_view(),
        name='session_delete_other',
    ),
    url(
        regex=r'^account/sessions/(?P<pk>\w+)/delete/$',
        view=CustomSessionDeleteView.as_view(),
        name='session_delete',
    ),
]