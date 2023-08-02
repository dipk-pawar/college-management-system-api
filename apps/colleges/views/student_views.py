from rest_framework.response import Response
from rest_framework import status, generics
from apps.common.error_helper import FormatError
from rest_framework.permissions import IsAuthenticated
from apps.accounts.models import User
from apps.accounts.serializers.user_serializer import UserSerializer


class CollegeUserList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.all()
        if user.role_id != 1:
            role_id = self.request.query_params.get("role_id", None)
            if role_id is not None:
                queryset = queryset.filter(
                    role_id=int(role_id), college_id=user.college.id
                )
        return queryset
