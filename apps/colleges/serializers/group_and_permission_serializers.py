# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from apps.colleges.models import CollegeGroup
from apps.common.helpers.user_helper import GenerateRandomChar
from django.db import IntegrityError


class CollegeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeGroup
        fields = ["id", "group_name"]
        extra_kwargs = {
            "id": {"read_only": True},
        }

    def validate(self, attrs):
        group_name = attrs.get("group_name")
        if len(group_name) <= 2:
            raise serializers.ValidationError(
                {"message": "Length of group name must be Greater then 2"}
            )
        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request else None
        group_name = validated_data["group_name"]
        name = GenerateRandomChar.generate_username(group_name)
        try:
            return CollegeGroup.objects.create(
                name=name, group_name=group_name, college_id=user.college.id
            )
        except IntegrityError as e:
            raise serializers.ValidationError(
                {"message": "Group name already exists for this college"}
            ) from e

    def to_representation(self, instance):
        group_data = super().to_representation(instance)
        group_data["permissions"] = Group.objects.filter(
            permissions__in=instance.permissions.all()
        ).values(
            "permissions__id",
            "permissions__codename",
            "permissions__name",
            "permissions__content_type_id",
        )
        return group_data


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "name", "content_type_id", "codename"]

    # def to_representation(self, instance):
    #     permission_data = super().to_representation(instance)
    #     print(permission_data)
