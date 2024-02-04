import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from .ws_urls import ws_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_clone.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": URLRouter(ws_urlpatterns)
})
