from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from apps.accounts.serializers.user_serializer import LoginSerializer, UserSerializer
from apps.common.error_helper import FormatError
from cms.jwt_custom_token import get_tokens_for_user
from django.db import transaction
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.common.permissions import SuperUserORAdmin


# Create your views here.
class Login(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "error": True,
                    "message": FormatError.format_serializer_errors(
                        errors=serializer.errors
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.validated_data["user"]
        tokens = get_tokens_for_user(user=user)

        return Response(
            {
                "error": False,
                "message": "Login successfully",
                "email": request.data.get("email"),
                "tokens": tokens,
            },
            status=status.HTTP_200_OK,
        )


class RegisterUser(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, SuperUserORAdmin)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "error": True,
                    "message": FormatError.format_serializer_errors(
                        errors=serializer.errors
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()

        # check it university id is available
        return Response(
            status=status.HTTP_201_CREATED,
            data={
                "error": False,
                "data": serializer.data,
                "message": "User created successfully",
            },
        )
