from rest_framework.response import Response
from rest_framework import status, generics
from apps.colleges.serializers.college_serializers import (
    CreateCollegeSerializer,
    CollegeSerializer,
    ReadCollegeAndAdminSerializer,
)
from apps.common.error_helper import FormatError
from apps.common.helpers.user_helper import GeneratePassword
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from apps.colleges.signals import college_signal
from apps.colleges.models import College


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
        request.data["password"] = GeneratePassword.generate_password(12)
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
