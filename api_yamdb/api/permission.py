from rest_framework import permissions


class IsAuthenticatedAdminOrReadOnly(permissions.BasePermission):
    """Аутентифицированный администратор или только чтение."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )


class IsAdminOrModeratorOrAuthor(permissions.BasePermission):
    """Для автора, модератора и админа доступны небезопасные запросы."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (
                request.user.is_admin
                or request.user.is_moderator
                or request.user == obj.author
            )
        )
