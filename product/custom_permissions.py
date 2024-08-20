from rest_framework import permissions

class IsStaff(permissions.BasePermission):
    """
    Permission для проверки флага is_staff
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)
