# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from apps.colleges.models import CollegeGroup
from apps.common.helpers.user_helper import GenerateRandomChar
from django.db import IntegrityError
from apps.common.constant import ModelsName


class CollegeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeGroup
        fields = ["id", "group_name", "permissions"]
        extra_kwargs = {
            "id": {"read_only": True},
            "group_name": {"required": True},
            "permissions": {"required": True},
        }

    def validate(self, attrs):
        request_user = self.context.get("request").user
        group_name = attrs.get("group_name")
        permissions = attrs.get("permissions")
        if len(group_name) <= 2:
            raise serializers.ValidationError(
                {"message": "Length of group name must be Greater then 2"}
            )
        if len(permissions) == 0:
            raise serializers.ValidationError(
                {"message": "Please assign atlist 1 permission"}
            )
        permissions_list = list(map(lambda permission: permission.id, permissions))
        if not request_user.is_superuser:
            allowed_user_permissions = list(
                Permission.objects.filter(
                    content_type__model__in=ModelsName.allow_models
                ).values_list("id", flat=True)
            )

            for permission in permissions_list:
                if permission not in allowed_user_permissions:
                    raise serializers.ValidationError(
                        {
                            "message": f"Sorry, can not assign the permission {permission}"
                        }
                    )

        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request else None
        group_name = validated_data["group_name"]
        permissions = validated_data["permissions"]
        name = GenerateRandomChar.generate_username(group_name)
        try:
            college_group = CollegeGroup.objects.create(
                name=name, group_name=group_name, college_id=user.college.id
            )
            college_group.permissions.set(permissions)
            return college_group
        except IntegrityError as e:
            raise serializers.ValidationError(
                {"message": "Group name already exists for this college"}
            ) from e

    def to_representation(self, instance):
        group_data = super().to_representation(instance)
        group_data["permissions"] = Permission.objects.filter(
            id__in=group_data["permissions"]
        ).values(
            "id",
            "codename",
            "name",
            "content_type_id",
        )
        return group_data


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "name", "content_type_id", "codename"]
