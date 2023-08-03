# views.py
from rest_framework import viewsets
from apps.colleges.serializers.group_and_permission_serializers import (
    CollegeGroupSerializer,
)
from apps.common.permissions import SuperUserORAdmin
from apps.colleges.models import CollegeGroup


class CollegeGroupViewSet(viewsets.ModelViewSet):
    permission_classes = (SuperUserORAdmin,)
    serializer_class = CollegeGroupSerializer

    def get_queryset(self):
        queryset = CollegeGroup.objects.all()
        user = self.request.user
        if not user.is_superuser:
            queryset = queryset.filter(college_id=user.college.id)
        return queryset
