from user.utilities.ip_utilities import UserIpUtility
from user.models import UserActivity


class UserActivityQuerySet:

    @staticmethod
    def create(user, request):
        data = {
            "user_agent": request.META.get("HTTP_USER_AGENT"),
            "user": user,
            "ip_address": UserIpUtility.get_client_ip(request),
            "country_code": UserIpUtility.get_country_from_request(request),
        }
        return UserActivity.objects.create(**data)
