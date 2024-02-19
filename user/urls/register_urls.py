from django.urls import path
from user.views import RegisterBySystem
from user.views.user_register_by_google import RegisterByGoogleAPIView

from user.views.user_register_by_facebook import RegisterByFacebookAPIView

urlpatterns = [
    path("system", RegisterBySystem.as_view(), name="register-by-system-api"),
    path("facebook", RegisterByFacebookAPIView.as_view(), name="register-by-facebook-api"),
    path("google", RegisterByGoogleAPIView.as_view(), name="register-by-google-api"),
]
