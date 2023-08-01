from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from apps.accounts.serializers.user_serializer import LoginSerializer
from apps.common.error_helper import FormatError
from cms.jwt_custom_token import get_tokens_for_user


# Create your views here.
class Login(APIView):
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
