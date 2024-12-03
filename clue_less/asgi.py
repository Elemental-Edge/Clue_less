"""
ASGI config for clue_less project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clue_less.settings")

# Ensure apps are loaded before importing application-specific modules
django_asgi_app = get_asgi_application()

# Import application-specific routing after the apps are ready
from Backend.MessageTranslator import routing as message_routing  # Import your app's routing file

# Define the ASGI application
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            message_routing.websocket_urlpatterns  # Define WebSocket URLs in routing.py
        )
    ),
})
