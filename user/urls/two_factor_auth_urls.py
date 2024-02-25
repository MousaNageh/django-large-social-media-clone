from django.urls import path
from user.views.two_factor_auth_views import TwoFactorAuthByEmailAPIView


urlpatterns = [
    path("email", TwoFactorAuthByEmailAPIView.as_view(), name="2fa-by-email-api")
]
