from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from user.serializers import RegisterBySystemSerializer


class RegisterBySystem(APIView):

    @classmethod
    def post(cls, request):
        serializer = cls._serialize_register_request(request)
        user = serializer.save()
        return Response({"email": user.email}, status=HTTP_201_CREATED)

    @staticmethod
    def _serialize_register_request(request):
        serializer = RegisterBySystemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer
