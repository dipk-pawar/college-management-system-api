from rest_framework import serializers
from apps.accounts.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import authenticate
from apps.colleges.serializers.college_serializers import (
    CollegeSerializer,
    RoleSerializer,
    CourseSerializer,
)
from apps.common.helpers.custom_exeception_helper import ExceptionError
from apps.colleges.models import Course, Role


def validate_email_address(email):
    try:
        validate_email(email)
    except ValidationError as e:
        raise serializers.ValidationError(
            {"error": "Email is not valid"}, code="authorization"
        ) from e
    return email


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"})

    def is_valid(self, raise_exception=False):
        email = self.initial_data.get("email")
        try:
            validate_email(email)
        except:
            raise ExceptionError("Email is not valid")
        return super(LoginSerializer, self).is_valid(raise_exception=raise_exception)

    def validate(self, attrs):
        email = attrs.get("email")
        user = User.objects.filter(email=email).first()

        if not user:
            raise ExceptionError("Unable to log in with provided credentials.")

        if not user.is_active:
            raise ExceptionError(
                "Your account is not active please contact admin for more details."
            )
        password = attrs.get("password")
        user = authenticate(email=email, password=password)
        if not user:
            raise ExceptionError("Unable to log in with provided credentials.")
        attrs["user"] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    college = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "college",
            "role",
            "courses",
        ]

        extra_kwargs = {
            "id": {"read_only": True},
            "email": {"write_only": True},
            "password": {"write_only": True},
            "is_staff": {"read_only": True},
            "is_admin": {"read_only": True},
            "is_superuser": {"read_only": True},
        }

    def is_valid(self, raise_exception=False):
        request_user = self.context.get("request").user
        role_id = self.initial_data.get("role")
        roles = list(
            Role.objects.filter(college_id=request_user.college_id).values_list(
                "id", flat=True
            )
        )
        if role_id not in roles:
            raise ExceptionError(
                "Sorry, role not found. Create a role before assigning it."
            )
        courses = self.initial_data.get("courses")
        college_courses = list(
            Course.objects.filter(college_id=request_user.college_id).values_list(
                "id", flat=True
            )
        )
        for course in courses:
            if course not in college_courses:
                raise ExceptionError("Sorry, course not found.")
        return super(UserSerializer, self).is_valid(raise_exception=raise_exception)

    def get_college(self, obj):
        request = self.context.get("request")
        return CollegeSerializer(request.user.college).data if request else None

    def to_representation(self, instance):
        user_data = super().to_representation(instance)
        user_data["courses"] = CourseSerializer(instance.courses.all(), many=True).data
        user_data["role"] = (
            RoleSerializer(instance.role).data if instance.role else None
        )
        user_data["role"]["college"] = instance.college.id
        return user_data
