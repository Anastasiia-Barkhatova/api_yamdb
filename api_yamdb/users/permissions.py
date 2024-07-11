from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

class IsModeratorUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user or request.user.is_moderator or request.user.is_admin

class IsAdminOrSelf(permissions.BasePermission):
    def has_permission(self, request, view):
        # Разрешить GET запросы всем аутентифицированным пользователям
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        # Запретить все изменения, кроме администраторов и владельцев профиля
        return request.user.is_authenticated and (request.user.is_admin or request.user.username == view.kwargs.get('username'))


class IsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user
