from django.urls import path
from user.views.login_views import LoginAPIView


urlpatterns = [path("", LoginAPIView.as_view(), name="login-api")]
