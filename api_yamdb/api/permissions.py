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


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'moderator'
