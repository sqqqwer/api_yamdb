import random
import string

from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives, send_mail
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import response, status, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import IsAuthorOrReadOnly, UserEmail, CorrectToken
from api.serializers import ReviewSerializer, EmailValidationSerializer, TokenSerializer
from yamdb.models import Review

User = get_user_model()


# временный класс для тестов
class CommentViewSet(viewsets.ModelViewSet):
    pass


# временный класс для тестов
class TitleViewSet(viewsets.ModelViewSet):
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с отзывами."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)


class EmailValidationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = EmailValidationSerializer
    permission_classes = (UserEmail,)

    def perform_create(self, serializer):
        confirmation_code = ''.join(random.choice(string.ascii_letters) for i in range(5))

        msg = EmailMultiAlternatives(
            "Subject here",
            confirmation_code,
            "from@example.com",
            [get_object_or_404(User, self.request.user).email],
        )
        msg.send()
        serializer.save(confirmation_code=confirmation_code)


class TokenViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = TokenSerializer
    permission_classes = (CorrectToken,)
