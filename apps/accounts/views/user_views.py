from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from apps.accounts.serializers.user_serializer import LoginSerializer, UserSerializer
from apps.common.helpers.user_helper import GenerateRandomChar
from cms.jwt_custom_token import get_tokens_for_user
from django.db import transaction
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.common.permissions import SuperUserORAdmin
from apps.common.helpers.error_decorator import track_error
from django.contrib.auth.hashers import make_password


# Create your views here.
class Login(APIView):
    permission_classes = (AllowAny,)

    @track_error(validate_api_parameters=["email", "password"])
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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

    @track_error(
        validate_api_parameters=["email", "first_name", "last_name", "role", "courses"]
    )
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = GenerateRandomChar.generate_password(12)
        user = serializer.save(
            college_id=request.user.college_id, password=make_password(password)
        )
        user.courses.set(request.data.get("courses"))

        return Response(
            status=status.HTTP_201_CREATED,
            data={
                "error": False,
                "data": {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "password": password,
                    "college": user.college.name,
                    "role": user.role.name,
                },
                "message": "User created successfully",
            },
        )
