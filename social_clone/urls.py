from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


api_urlpatterns = [
    path("register/", include("user.urls.register_urls")),
    path("login/", include("user.urls.login_urls")),
    path("2fa/", include("user.urls.two_factor_auth_urls")),
]

urlpatterns = (
    [
        path("swagger/", include("social_clone.swagger_urls")),
        path("api/", include(api_urlpatterns)),
        path("admin/", admin.site.urls),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

if settings.DEBUG:
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]

ASGI_APPLICATION = "social_clone.asgi.application"
