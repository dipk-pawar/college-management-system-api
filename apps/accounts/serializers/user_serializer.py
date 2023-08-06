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
from apps.common.helpers.user_helper import GenerateRandomChar
from apps.colleges.models import Role


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

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError(
                {"error": 'Must include "email" and "password".'},
                code="authorization",
            )

        email = validate_email_address(email)
        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError(
                {"error": "Unable to log in with provided credentials."},
                code="authentication_failed",
            )

        if not user.is_active:
            raise serializers.ValidationError(
                {
                    "error": "Your account is not active please contact admin for more details."
                },
                code="authentication_failed",
            )

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError(
                {"error": "Unable to log in with provided credentials."},
                code="authentication_failed",
            )

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
            "college": {"required": True},
            "role": {"required": True},
            "courses": {"required": True},
        }

    def to_internal_value(self, data):
        role_id = data.get("role")
        if role_id is not None:
            request_user = self.context.get("request").user
            roles = list(
                Role.objects.filter(college_id=request_user.college.id).values_list(
                    "id", flat=True
                )
            )
            if role_id not in roles:
                raise serializers.ValidationError(
                    {
                        "role": "Sorry, role not found. Create a role before assigning it."
                    }
                )

        return super().to_internal_value(data)

    def get_college(self, obj):
        request = self.context.get("request")
        return CollegeSerializer(request.user.college).data if request else None

    def create(self, validated_data):
        request = self.context.get("request")
        courses = validated_data.get("courses", None)
        validated_data["college"] = request.user.college
        validated_data.pop("courses", None)
        validated_data["password"] = GenerateRandomChar.generate_password(12)
        user = User.objects.create_user(**validated_data)
        if courses:
            user.courses.set(courses)
        return user

    def to_representation(self, instance):
        user_data = super().to_representation(instance)
        user_data["courses"] = CourseSerializer(instance.courses.all(), many=True).data
        user_data["role"] = (
            RoleSerializer(instance.role).data if instance.role else None
        )
        user_data["role"]["college"] = instance.college.id
        return user_data
