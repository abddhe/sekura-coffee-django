from django.urls import path
from . import consumers
#urls to notificcation
websocket_urlpatterns = [
    path("notifications", consumers.NotificationConsumer.as_asgi())
]
