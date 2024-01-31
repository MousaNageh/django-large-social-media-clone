from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

api_urlpatterns = []

urlpatterns = (
    [
        path("api/", include(api_urlpatterns)),
        path("admin/", admin.site.urls),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

if settings.DEBUG:
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]

ASGI_APPLICATION = "social_clone.asgi.application"