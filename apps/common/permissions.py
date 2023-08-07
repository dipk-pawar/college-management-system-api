# permissions.py

from rest_framework.permissions import BasePermission


class SuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_superuser)


class SuperUserORAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_superuser or request.user.is_college_admin)


class APIPermission(BasePermission):
    def get_queryset_model_name(self, view):
        # Get the queryset attribute from the view and return the model name
        if hasattr(view, "queryset") and view.queryset is not None:
            return view.queryset.model.__name__
        elif hasattr(view, "get_queryset") and view.get_queryset is not None:
            return view.get_queryset().model.__name__
        return None

    def has_group_permission(self, user, permission_code):
        user_groups = user.groups.all()
        return any(
            group.permissions.filter(codename=permission_code.lower()).exists()
            for group in user_groups
        )

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        model_name = self.get_queryset_model_name(view)
        permission_codes = {
            "GET": f"view_{model_name}",
            "POST": f"add_{model_name}",
            "PUT": f"change_{model_name}",
            "DELETE": f"delete_{model_name}",
        }

        # Get the required permission code based on the requested method
        required_permission = permission_codes.get(request.method)

        if _ := self.has_group_permission(request.user, required_permission):
            return True

        """If the user doesn't have the required group permission, 
        check if they have an individual permission"""
        return bool(request.user.has_api_permissions(perm=required_permission))
