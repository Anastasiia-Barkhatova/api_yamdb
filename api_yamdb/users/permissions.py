from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """Разрешение для администраторов."""

    def has_permission(self, request, view):
        """
        Проверка, что пользователь аутентифицирован.

        и является администратором.
        """
        return request.user.is_authenticated and request.user.is_admin


class IsModeratorUser(permissions.BasePermission):
    """Разрешение для модераторов."""

    def has_permission(self, request, view):
        """
        Проверка, что пользователь аутентифицирован.

        и является модератором.
        """
        return request.user.is_authenticated and request.user.is_moderator


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешение для автора объекта.

    или только чтение для других.
    """

    def has_permission(self, request, view):
        """
        Разрешение на чтение для всех.

        на изменение только для аутентифицированных пользователей.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Разрешение на чтение для всех.

        на изменение только для автора, модератора или администратора.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )


class IsAdminOrSelf(permissions.BasePermission):
    """Разрешение для администратора или самого пользователя."""

    def has_permission(self, request, view):
        """
        Разрешение на чтение для аутентифицированных пользователей.

        на изменение только для администратора или самого пользователя.
        """
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        return request.user.is_authenticated and (
            request.user.is_admin
            or request.user.username == view.kwargs.get('username')
        )


class IsSelf(permissions.BasePermission):
    """Разрешение только для самого пользователя."""

    def has_object_permission(self, request, view, obj):
        """Проверка, что объект принадлежит текущему пользователю."""
        return obj == request.user
