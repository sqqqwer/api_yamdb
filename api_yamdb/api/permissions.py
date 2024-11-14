from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions

User = get_user_model()


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Пермишн, который дает доступ на редактрование только авторам.""" 
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
