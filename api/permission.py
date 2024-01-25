
from rest_framework import permissions

class IsAdminOrStaffUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow read-only access for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        # Allow editing and deleting for admin or staff users
        return request.user and (request.user.is_staff or request.user.is_superuser)
