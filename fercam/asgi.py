"""
ASGI config for fercam project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fercam.settings")

import django
django.setup()

from django.core.management import call_command


from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import transport.routing
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fercam.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                transport.routing.websocket_urlpatterns
            )
        )
    ), 
})
