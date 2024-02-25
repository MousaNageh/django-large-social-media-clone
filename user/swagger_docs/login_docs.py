from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from user.serializers.login_serializers import LoginSerializer


def login_docs():
    return swagger_auto_schema(
        operation_summary="login by username or email and password",
        request_body=LoginSerializer,
        operation_description="login by username or email and password",
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "refresh": openapi.Schema(
                            type=openapi.TYPE_STRING, description="access token"
                        ),
                        "access": openapi.Schema(
                            type=openapi.TYPE_STRING, description="refresh token"
                        ),
                    },
                ),
            ),
            400: "Bad Request",
        },
    )
