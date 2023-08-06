from django.db import IntegrityError
from rest_framework import serializers
from apps.colleges.models import College, Role, Course
from apps.accounts.models import User


class CreateCollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ["id", "name", "location"]
        extra_kwargs = {
            "id": {"read_only": True},
        }

    def create(self, validated_data):
        return College.objects.create(
            name=validated_data.get("name"), location=validated_data.get("location")
        )


class ReadCollegeAndAdminSerializer(serializers.ModelSerializer):
    college_admin = serializers.SerializerMethodField()

    class Meta:
        model = College
        fields = [
            "id",
            "name",
            "location",
            "established_date",
            "description",
            "college_admin",
        ]

    def get_college_admin(self, instance):
        return User.objects.filter(
            college_id=instance.id, is_college_admin=True
        ).values("id", "first_name", "last_name", "email")


class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = "__all__"


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name"]
        extra_kwargs = {"id": {"read_only": True}, "name": {"required": True}}

    def create(self, validated_data):
        user = self.context.get("request").user
        try:
            return Role.objects.create(
                name=validated_data.get("name"), college_id=user.college.id
            )
        except IntegrityError as e:
            raise serializers.ValidationError(
                {
                    "error": f"Role name {validated_data.get('name')} already exists for this college"
                }
            ) from e


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
