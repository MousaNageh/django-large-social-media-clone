from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from user.serializers import RegisterBySystemSerializer
from user.querysets.opt_queryset import OTPQuerySet
from user.serializers.user_register_by_system_serializers import ResendOTPSerializer, VerifyEmailSerializer
from user.tasks import send_register_email
from django.db import transaction


class RegisterBySystem(APIView):

    @classmethod
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
    def put(cls, request):
        serializer = ResendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        cls._send_opt(user.get("id"), user.get("email"))
        return Response({"ok": f"an email has been send to {user.get('email')}"})

    @classmethod
    def patch(cls, request):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"user_activated": f"user with email '{user.get('email')}' now activated"})



    @staticmethod
    def _serialize_register_request(request):
        serializer = RegisterBySystemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer

    @staticmethod
    def _send_opt(user_id, user_email):
        opt = OTPQuerySet.create_or_replace_otp(user_id)
        send_register_email.delay(opt.code, user_email)
