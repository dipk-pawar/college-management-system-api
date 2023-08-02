# permissions.py

from rest_framework.permissions import BasePermission


class ObjectPermission(BasePermission):
    def get_queryset_model_name(self, view):
        # Get the queryset attribute from the view and return the model name
        if hasattr(view, "queryset") and view.queryset is not None:
            return view.queryset.model.__name__
        elif hasattr(view, "get_queryset") and view.get_queryset is not None:
            return view.get_queryset().model.__name__
        return None

    def has_permission(self, request, view):
        model_name = self.get_queryset_model_name(view)
        import pdb

        pdb.set_trace()
        permission_codes = {
            "GET": f"view_{model_name}",
            "POST": f"add_{model_name}",
            "PUT": f"change_{model_name}",
            "DELETE": f"delete_{model_name}",
        }

        # Get the required permission code based on the requested method
        required_permission = permission_codes.get(request.method)

        # Check if the user has the required permission in their group
        has_required_group_permission = self.has_group_permission(
            request.user, required_permission
        )

        # If the user has the required group permission, allow access
        if has_required_group_permission:
            return True

        # If the user doesn't have the required group permission,
        # check if they have an individual permission
        if request.user.has_perm(required_permission):
            return True

        # If neither group nor individual permission allows access, deny it
        return False

    def has_group_permission(self, user, permission_code):
        return user.groups.filter(permissions__codename=permission_code).exists()
