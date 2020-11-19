import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import transport.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fercam.settings")

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            transport.routing.websocket_urlpatterns
        )
    ),
})
