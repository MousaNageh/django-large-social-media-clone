from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated

from user.serializers.two_factor_auth_serializers import (
    TwoFactorAuthSerializerByEmailSerializer,
)


class TwoFactorAuthByEmailAPIView(
    generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin
):
    permission_classes = [IsAuthenticated]
    serializer_class = TwoFactorAuthSerializerByEmailSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
