"""Разрешения приложения 'api'."""
from rest_framework import permissions
from rest_framework.views import exceptions


class AdminOrReadOnly(permissions.BasePermission):
    """Разрешения для чтения записей любым пользователем и создания,
    изменения и удаления записей администратором и суперпользователем."""

    def has_permission(self, request, view):
        """Функция разрешений на уровне запроса."""
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_admin:
                return True
        return False


class AuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if (request.user.is_superuser or request.user.is_admin
                or request.user.is_moderator):
            return True
        if obj.author == request.user:
            return True
        return False


class OnlyAdmin(permissions.BasePermission):
    """Зона управления пользователями для админов"""
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated and request.user.is_admin:
            return True
        return False


class OnlyAdminCanGiveRole(permissions.BasePermission):
    """Поле role может менять себе и другием только админ."""
    def has_permission(self, request, view,):
        if request.user.is_anonymous:
            raise exceptions.NotAuthenticated()
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.data.get('role') and request.user.is_admin:
            return True
        if not request.data.get('role'):
            return True
        else:
            raise exceptions.NotAuthenticated(detail={"role": 'user'})
