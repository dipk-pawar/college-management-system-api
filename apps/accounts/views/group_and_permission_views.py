# views.py
from rest_framework import viewsets
from django.contrib.auth.models import Group
from apps.accounts.serializers.group_and_permission_serializers import GroupSerializer
from apps.common.permissions import SuperUserORAdmin


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = (SuperUserORAdmin,)
    serializer_class = GroupSerializer

    def get_queryset(self):
        queryset = Group.objects.all()
        user = self.request.user
        print(user)
        # if not user.is_superuser:
        #         queryset = queryset.filter(
        #             college_id=int(role_id), college_id=user.college.id
        #         )
        return queryset
