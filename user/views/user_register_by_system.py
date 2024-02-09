from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR
from user.serializers import RegisterBySystemSerializer
from user.querysets.opt_queryset import OPTQuerySet
from user.tasks import send_register_email
from django.db import transaction


class RegisterBySystem(APIView):

    @classmethod
    def post(cls, request):
        serializer = cls._serialize_register_request(request)
        try:
            with transaction.atomic():
                user = serializer.save()
                cls._send_opt(user)
        except Exception as e:
            return Response(
                {"server_error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response({"email": user.email}, status=HTTP_201_CREATED)

    @staticmethod
    def _serialize_register_request(request):
        serializer = RegisterBySystemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer

    @staticmethod
    def _send_opt(user):
        opt = OPTQuerySet.create_or_replace_otp(user.id)
        send_register_email.delay(opt.code, user.email)
