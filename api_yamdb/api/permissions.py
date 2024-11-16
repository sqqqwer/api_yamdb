from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Пермишн, который дает доступ на редактрование только авторам,
    админам, модераторам. А безопасные методы пропускает.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            or request.method in permissions.SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.admin
            or request.user.moderator
        )


class IsRoleAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role == 'admin')


class IsRoleAdminOrReadOnly(IsRoleAdmin):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or super().has_permission(request, view))


class IsRoleModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role == 'moderator')


class IsRoleModeratorOrReadOnly(IsRoleModerator):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or super().has_permission(request, view))
