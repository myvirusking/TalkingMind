from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from blog.consumers import NotificationConsumer



application = ProtocolTypeRouter({
    # (http->django views is added by default)
    "websocket": URLRouter([
        path("ws/",NotificationConsumer),
    ])
})