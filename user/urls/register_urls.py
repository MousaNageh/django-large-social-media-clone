from django.urls import path
from user.views import RegisterBySystem

urlpatterns = [
    path("system", RegisterBySystem.as_view(), name="register-by-system-api")
]
