from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from user.serializers.register_by_facebook_serializers import RegisterByFacebookSerializer


def register_by_facebook_docs():
    return swagger_auto_schema(
        operation_summary="register or login by facebook",
        request_body=RegisterByFacebookSerializer,
        operation_description="register or login by facebook",
        responses={
            201: openapi.Response(
                description="Successful response",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "access": openapi.Schema(type=openapi.TYPE_STRING),
                        "refresh": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            400: "Bad Request",
        },
    )
