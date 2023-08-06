from rest_framework.response import Response
from rest_framework import status, generics
from apps.colleges.serializers.student_serializers import SubjectSerializer
from apps.common.error_helper import FormatError
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from apps.common.permissions import APIPermission
from apps.colleges.models import Subject


class CourseList(generics.ListAPIView):
    serializer_class = SubjectSerializer

    def get_queryset(self):
        user = self.request.user
        return (
            Subject.objects.all()
            if user.is_superuser
            else Subject.objects.filter(
                college_id=user.college_id, course__in=user.courses.all()
            )
        )
