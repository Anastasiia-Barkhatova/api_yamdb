from rest_framework import permissions


class IsAuthenticatedOrAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdminOrModeratorOrAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (
                request.user.is_staff
                or request.user.is_admin
                or request.user.is_moderator
                or request.user == obj.author
            )
        )
