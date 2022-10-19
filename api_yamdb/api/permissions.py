from rest_framework import permissions


class IsAdminOrSuperUser(permissions.BasePermission):
    """
    Grants permission to manage data to SuperUser and Admin users.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )


class IsModeratorOrAdminOrOwner(permissions.BasePermission):
    """
    Grants permission to manage individual data
    to data owner, SuperUser, Admin and Moderator users.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user
            )
        )
