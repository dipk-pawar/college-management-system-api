# views.py
from rest_framework import viewsets, generics
from apps.colleges.serializers.group_and_permission_serializers import (
    CollegeGroupSerializer,
    PermissionSerializer,
)
from apps.common.permissions import SuperUserORAdmin
from apps.colleges.models import CollegeGroup
from django.contrib.auth.models import Permission
from apps.common.constant import ModelsName


class CollegeGroupViewSet(viewsets.ModelViewSet):
    permission_classes = (SuperUserORAdmin,)
    serializer_class = CollegeGroupSerializer

    def get_queryset(self):
        queryset = CollegeGroup.objects.all()
        user = self.request.user
        if not user.is_superuser:
            queryset = queryset.filter(college_id=user.college.id)
        return queryset


class PermissionListView(generics.ListAPIView):
    serializer_class = PermissionSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Permission.objects.all()
        return Permission.objects.filter(
            content_type__model__in=ModelsName.allow_models
        )


# class PermissionListView(APIView):
#     def get(self, request):
#         # List of models you want to show permissions for
#         allowed_models = [User, College, Course, Role]

#         # Filter permissions based on the allowed models
#         permissions = Permission.objects.filter(content_type__model__in=allowed_models)
#         serializer = PermissionSerializer(permissions, many=True)
#         return Response(serializer.data)
