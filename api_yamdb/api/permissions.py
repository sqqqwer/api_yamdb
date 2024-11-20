from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsAuthorOrStaff(permissions.BasePermission):
    """Пермишн, который дает доступ на редактрование авторам.

    Пропускает: авторов, модераторов, админов и если безопастный метод.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )


class IsRoleAdmin(permissions.BasePermission):
    """Пермишн, который пропускает только админов."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin)


class IsRoleAdminOrReadOnly(IsRoleAdmin):
    """Пермишн, который пропускает только если метод безопасный или админов."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or super().has_permission(request, view))
