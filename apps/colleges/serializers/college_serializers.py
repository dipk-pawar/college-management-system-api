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
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
