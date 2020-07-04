from axes.backends import AxesBackend
from axes.helpers import toggleable
from Blogging import settings


class CustomAxesBackend(AxesBackend):

    @toggleable
    def authenticate(self, request, username: str = None, password: str = None, **kwargs: dict):
        settings.CURRENT_USER = username
        print("This is userbnae",username)
        return super(CustomAxesBackend, self).authenticate(request, username, password, **kwargs)
