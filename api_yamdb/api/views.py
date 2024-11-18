from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import (SAFE_METHODS, AllowAny, IsAdminUser,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api import serializers
from api.filters import TitleFilter
from api.mixins import MixinTagViewSet
from api.permissions import IsAuthorOrStaff, IsRoleAdmin, IsRoleAdminOrReadOnly
from reviews.models import Category, Genre, Review, Title

User = get_user_model()


class RegistrationView(CreateAPIView):
    """APIview для создания пользователя."""

    queryset = User.objects.all()
    serializer_class = serializers.RegistrationSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = super().get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = super().get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK,
                        headers=headers)


class TokenView(CreateAPIView):
    """APIview для получения токена."""

    serializer_class = serializers.TokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = super().get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=serializer.validated_data['username'])
        token = str(AccessToken.for_user(user))
        return Response({'token': token}, status=status.HTTP_200_OK)


class UserMeView(RetrieveUpdateAPIView):
    """APIview для получения и редактирования своей учетной записи."""

    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = serializers.UserMeSerializer

    def get_object(self):
        return self.request.user


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с пользователями."""

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (IsRoleAdmin | IsAdminUser,)
    filter_backends = (SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с отзывами."""

    permission_classes = (IsAuthorOrStaff, IsAuthenticatedOrReadOnly)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title_obj(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title

    def get_queryset(self):
        title = self.get_title_obj()
        return title.reviews.all()

    def get_serializer_class(self):
        if self.request.method not in SAFE_METHODS:
            return serializers.PostPatchReviewSerializer
        return serializers.GetReviewSerializer

    def perform_create(self, serializer):
        title = self.get_title_obj()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с комментариями."""

    serializer_class = serializers.CommentSerializer
    permission_classes = (IsAuthorOrStaff, IsAuthenticatedOrReadOnly)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review_obj(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(
            Review.objects.filter(title=title), pk=review_id)

    def get_queryset(self):
        review = self.get_review_obj()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_review_obj()
        serializer.save(author=self.request.user, review=review)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с произведениями."""

    queryset = Title.objects.all()
    permission_classes = (IsRoleAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    ordering_fields = ('category', 'genre', 'name', 'year')
    ordering = ('-year',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method not in SAFE_METHODS:
            return serializers.PostPatchTitleSerializer
        return serializers.GetTitleSerializer


class CategoryViewSet(MixinTagViewSet):
    """Вьюсет для работы с категориями."""

    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class GenreViewSet(MixinTagViewSet):
    """Вьюсет для работы с жанрами."""

    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
