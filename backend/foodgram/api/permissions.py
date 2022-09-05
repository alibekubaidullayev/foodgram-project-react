from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, _):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, _):
        return request.user.is_authenticated and request.user.is_admin
