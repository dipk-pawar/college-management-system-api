from rest_framework import serializers
from apps.colleges.models import Subject
from apps.accounts.models import User


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"
