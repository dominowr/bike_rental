from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    """
    Custom permission to allow only superuser to view user detail and user list.
    """
    def has_permission(self, request, view):
        return request.user.is_superuser
