from rest_framework.permissions import BasePermission


class IsActiveStaff(BasePermission):
    """
    Allow access only to authenticated, active staff users.
    """
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_active
            and request.user.is_staff
        )
