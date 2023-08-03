from rest_framework.response import Response
from rest_framework import status, generics
from apps.common.error_helper import FormatError
from rest_framework.permissions import IsAuthenticated
from apps.accounts.models import User
from apps.accounts.serializers.user_serializer import UserSerializer
from apps.common.permissions import APIPermission


class CollegeUserList(generics.ListAPIView):
    permission_classes = (IsAuthenticated, APIPermission)
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        user = self.request.user
        print(user)
        if user.role_id != 1:
            role_id = self.request.query_params.get("role_id", None)
            if role_id is not None:
                queryset = queryset.filter(
                    role_id=int(role_id), college_id=user.college.id
                )
        return queryset
