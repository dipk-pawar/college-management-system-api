from rest_framework.response import Response
from rest_framework import status, generics
from apps.colleges.serializers.college_serializers import (
    CreateCollegeSerializer,
    CollegeSerializer,
    ReadCollegeAndAdminSerializer,
)
from apps.common.error_helper import FormatError
from apps.common.helpers.user_helper import GenerateRandomChar
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from apps.colleges.signals import college_signal
from apps.colleges.models import College
from apps.accounts.models import User
from apps.accounts.serializers.user_serializer import UserSerializer
from apps.common.permissions import APIPermission


class CreateCollege(generics.CreateAPIView):
    serializer_class = CreateCollegeSerializer
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        if any(
            field not in request.data for field in ["email", "first_name", "last_name"]
        ):
            return Response(
                {
                    "error": True,
                    "message": "email, first_name and last_name is required for admin user",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
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
        request.data["college_id"] = serializer.data.get("id")
        request.data["password"] = GenerateRandomChar.generate_password(12)
        college_signal.send(sender=College, request_data=request.data)

        return Response(
            status=status.HTTP_201_CREATED,
            data={
                "error": False,
                "data": request.data,
                "message": "College created successfully",
            },
        )


class CollegeList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CollegeSerializer
    queryset = College.objects.all()


class CollegeAndAdminList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReadCollegeAndAdminSerializer
    queryset = College.objects.all()


class CollegeUserList(generics.ListAPIView):
    permission_classes = (IsAuthenticated, APIPermission)
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        user = self.request.user
        if not user.is_superuser:
            role_id = self.request.query_params.get("role_id", None)
            if role_id is not None:
                queryset = queryset.filter(
                    role_id=int(role_id), college_id=user.college.id
                )
        return queryset
