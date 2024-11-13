from rest_framework import permissions


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
