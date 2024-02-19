from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from user.querysets.login_queryset import LoginQueryset
from user.serializers.register_by_google_serializers import RegisterByGoogleSerializer
from user.swagger_docs.register_by_google_docs import register_by_google_docs


class RegisterByGoogleAPIView(CreateAPIView):
    serializer_class = RegisterByGoogleSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(LoginQueryset.get_token_for_user(user), status=status.HTTP_200_OK, headers=headers)

    @register_by_google_docs()
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
