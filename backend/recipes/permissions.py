from rest_framework import permissions


class IsOwnerOrAdminOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_obj_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_superuser
        )
