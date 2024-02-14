from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from user.querysets.login_queryset import LoginQueryset
from user.serializers.login_serializers import LoginSerializer


class LoginAPIView(CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(LoginQueryset.get_token_for_user(user), status=status.HTTP_200_OK, headers=headers)
