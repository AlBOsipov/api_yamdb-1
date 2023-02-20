from rest_framework import permissions


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
