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


class UserEmail(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (get_object_or_404(User, username=request.user.username) ==
                get_object_or_404(User, username=request.user.email))


class CorrectToken(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (get_object_or_404(User, username=request.user.confirmation_code) ==
                request.confirmation_code)
