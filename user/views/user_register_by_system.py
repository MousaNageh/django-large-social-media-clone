from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR
from user.serializers import (
    RegisterBySystemSerializer,
    ResendOTPSerializer,
    VerifyEmailSerializer,
)
from user.querysets.otp_queryset import OTPQuerySet
from user.swagger_docs.register_docs import (
    create_user_docs,
    resend_user_otp_docs,
    active_user_docs,
)
from user.tasks import send_register_email
from django.db import transaction


class RegisterBySystem(APIView):

    @classmethod
    @create_user_docs()
    def post(cls, request):
        serializer = cls._serialize_register_request(request)
        try:
            with transaction.atomic():
                user = serializer.save()
                cls._send_opt(user.id, user.email)
        except Exception as e:
            return Response(
                {"server_error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(
            {"email": user.email, "username": user.username}, status=HTTP_201_CREATED
        )

    @classmethod
    @resend_user_otp_docs()
    def put(cls, request):
        serializer = ResendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        cls._send_opt(user.get("id"), user.get("email"))
        return Response({"ok": f"an email has been send to {user.get('email')}"})

    @classmethod
    @active_user_docs()
    def patch(cls, request):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"user_activated": f"user with email '{user.get('email')}' now activated"}
        )

    @staticmethod
    def _serialize_register_request(request):
        serializer = RegisterBySystemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer

    @staticmethod
    def _send_opt(user_id, user_email):
        opt = OTPQuerySet.create_or_replace_otp(user_id)
        send_register_email.delay(opt.code, user_email)
