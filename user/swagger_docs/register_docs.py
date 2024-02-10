from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from user.serializers import RegisterBySystemSerializer, ResendOTPSerializer, VerifyEmailSerializer


def create_user_docs():
    return swagger_auto_schema(
        operation_summary="Create new user by system",
        request_body=RegisterBySystemSerializer,
        operation_description="register by system, create new user. after success otp will send automatically",
        responses={
            201: openapi.Response(
                description="Successful response",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        # 'message': openapi.Schema(type=openapi.TYPE_STRING, description="Success message"),
                        'email': openapi.Schema(type=openapi.TYPE_STRING),
                        'username': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            400: 'Bad Request'
        },
    )


def resend_user_otp_docs():
    return swagger_auto_schema(
        operation_summary="resend otp to user",
        request_body=ResendOTPSerializer,
        operation_description="resend otp to user",
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'ok': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            400: 'Bad Request'
        },
    )


def active_user_docs():
    return swagger_auto_schema(
        operation_summary="activate user",
        request_body=VerifyEmailSerializer,
        operation_description="activate user",
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'user_activated': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            400: 'Bad Request'
        },
    )
