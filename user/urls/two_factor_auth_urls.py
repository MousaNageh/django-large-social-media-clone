from django.urls import path
from user.views.two_factor_auth_views import (
    TwoFactorAuthByEmailAPIView,
    ActivateTwoFactorAuthByEmailAPIView,
)


urlpatterns = [
    path("email", TwoFactorAuthByEmailAPIView.as_view(), name="2fa-by-email-api"),
    path(
        "email/activate",
        ActivateTwoFactorAuthByEmailAPIView.as_view(),
        name="2fa-by-email-activate-api",
    ),
]
