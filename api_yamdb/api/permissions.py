from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Проверка наличия прав администратора."""

    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated and user.is_admin:
            return True


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Проверка наличия прав. Анонимный пользователь
    может только всё просматривать.
    Изменять контент может только администратор или суперпользователь.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.is_admin or request.user.is_superuser)))


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    """
    Проверка наличия прав. Анонимный пользователь
    может только всё просматривать.
    Изменять контент может только администратор, модератор или автор.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)
