from axes.backends import AxesBackend
from axes.helpers import toggleable
from django.conf import settings


class CustomAxesBackend(AxesBackend):

    @toggleable
    def authenticate(self, request, username: str = None, password: str = None, **kwargs: dict):
        settings.CURRENT_USER = username
        return super(CustomAxesBackend, self).authenticate(request, username, password, **kwargs)
