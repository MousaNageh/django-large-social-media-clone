from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from user.querysets.two_factor_auth_queryset import TwoFactorAuthQuerySet
from user.serializers.two_factor_auth_email_serializers import (
    TwoFactorAuthSerializerByEmailSerializer,
    ActivateTwoFactorAuthByEmail,
)


class TwoFactorAuthByEmailAPIView(CreateModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TwoFactorAuthSerializerByEmailSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        instance = TwoFactorAuthQuerySet.resend_otp_email_for_user(user=request.user)
        if not instance:
            return Response(
                {"2fa_not_exists": "user does not create 2fa"},
                status=HTTP_400_BAD_REQUEST,
            )
        if instance.is_verified:
            return Response(
                {"2fa_verified": "user already verified 2fa with email"},
                status=HTTP_400_BAD_REQUEST,
            )
        return Response({"email_sent": "email has send successfully"})


class ActivateTwoFactorAuthByEmailAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ActivateTwoFactorAuthByEmail
