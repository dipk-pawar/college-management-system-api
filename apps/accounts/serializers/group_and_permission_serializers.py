# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"

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
