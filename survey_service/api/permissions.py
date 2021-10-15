from rest_framework import permissions


class IsSafe(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return False


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.username == '':
            return False
        return request.user.is_superuser