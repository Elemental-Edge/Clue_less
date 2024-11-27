from django.urls import re_path
from Backend.MessageTranslator import consumers  # Import the consumer


websocket_urlpatterns = [
    re_path(r"ws/notifications/$", consumers.NotificationConsumer.as_asgi())
]