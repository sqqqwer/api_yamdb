import random
import string

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
import jwt

from api.permissions import IsAuthorOrReadOnly
from api_yamdb.settings import SIMPLE_JWT
from yamdb.models import Review
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, GetTitleSerializer,
                             PostPatchTitleSerializer, ReviewSerializer,
                            RegistrationSerializer, TokenReturnSerializer,
                            TokenSerializer)
from yamdb.models import Category, Genre, Review, Title


User = get_user_model()


# временный класс для тестов
class CommentViewSet(viewsets.ModelViewSet):
    pass


# временный класс для тестов
class TitleViewSet(viewsets.ModelViewSet):
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с отзывами."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_title_obj(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        title = self.get_title_obj()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_title_obj()
        serializer.save(author=self.request.user, title=title)


class RegistrationView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    def perform_create(self, serializer):
        confirmation_code = ''.join(random.choice(string.ascii_letters) for i in range(5))
        msg = EmailMultiAlternatives(
            "Code of api_yamdb",
            confirmation_code,
            "from@example.com",  # тут не знаю, от кого
            [get_object_or_404(User, self.request.user).email],
        )
        msg.send()
        serializer.save(confirmation_code=confirmation_code)


# есть подозрение, что нам надо сделать так https://habr.com/ru/articles/793058/
class TokenView(CreateAPIView):
    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        #
        token = jwt.encode(
            payload={
                SIMPLE_JWT['USER_FIELD_ID']: get_object_or_404(User, username=request.data['username']).id
            },
            key=SIMPLE_JWT['SIGNING_KEY'],
            algorithm=SIMPLE_JWT['ALGORITHM']
        )
        serializer = TokenReturnSerializer(token=token)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = User


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с комментариями."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_review_obj(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id)

    def get_queryset(self):
        review = self.get_review_obj()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_review_obj()
        serializer.save(author=self.request.user, review=review)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с произведениями."""
    queryset = Title.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('put', 'patch', 'post'):
            return PostPatchTitleSerializer
        return GetTitleSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с категориями."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthorOrReadOnly,)


class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с жанрами."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthorOrReadOnly,)

