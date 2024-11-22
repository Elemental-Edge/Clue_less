from django.urls import re_path
from Backend.MessageTranslator import consumers  # Import the consumer


websocket_urlpatterns = [
    re_path(r"ws/notifications/$", consumers.NotificationConsumer.as_asgi()),
    re_path(r"ws/gameroom/<id>$", consumers.GameRoomConsumer.as_asgi()),
    re_path(r"ws/gameroom/<id>/chat/$", consumers.GameRoomChatConsumer.as_asgi()),
]
