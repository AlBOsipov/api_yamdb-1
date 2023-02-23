from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
        )


class UserPermission(BasePermission):
    """Проверка, что пользователь является модератором."""
    def has_permission(self, request, view):
        return request.user.role == 'user'


class ModeratorPermission(BasePermission):
    """Проверка, что пользователь является модератором."""
    def has_permission(self, request, view):
        return request.user.role == 'moderator'


class AdminPermission(BasePermission):
    """Проверка, что пользователь является модератором."""
    def has_permission(self, request, view):
        return request.user.role == 'admin' or request.user.is_superuser


class SuperPermission(BasePermission):
    """Проверка, что пользователь является модератором."""
    def has_permission(self, request, view):
        return request.user.role == request.user.is_superuser


class AuthorOrAdmin(permissions.BasePermission):
    """Разрешение доступа к /me/ автору и админу."""
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.role == 'admin'
            or obj.user.username == request.user.username
            # или or obj.user == request.user
            # если это не сработает, обращайся через request.path_info
        )


class AuthorOrModeratorOrAdminOrReadOnly(permissions.BasePermission):
    """Разрешение доступа автору, админу, модератору."""
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == 'moderator'
            or request.user.role == 'admin'
            or obj.author == request.user
        )


class IsAuthIsAdminPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class AdminOrReadOnly(permissions.BasePermission):
    """Разрешение доступа админу или чтение."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.role == 'admin'
        return False
