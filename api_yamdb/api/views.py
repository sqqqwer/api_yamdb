import random
import string

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, mixins
from rest_framework.permissions import AND, IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import IsAuthorOrReadOnly, IsRoleAdmin, IsRoleModerator, IsRoleAdminOrReadOnly
from api import serializers
from yamdb.models import Category, Genre, Review, Title


User = get_user_model()


class RegistrationView(CreateAPIView):
    """APIview для создания пользователя."""
    queryset = User.objects.all()
    serializer_class = serializers.RegistrationSerializer
    permission_classes = (AllowAny,)

    def _get_confirmation_code_and_send_email(self, email):
        confirmation_code = ''.join([random.choice(string.ascii_letters)
                                    for _ in range(40)])
        send_mail(
            subject='Code of api_yamdb',
            message=confirmation_code,
            from_email='from@example.com',
            recipient_list=[email],
        )
        return confirmation_code

    def perform_create(self, serializer):
        confirmation_code = self._get_confirmation_code_and_send_email(
            serializer.validated_data['email']
        )

        serializer.save(confirmation_code=confirmation_code)

    def create(self, request, *args, **kwargs):
        serializer = super().get_serializer(data=request.data)
        user = User.objects.filter(
            username=self.request.data.get('username', '')).first()
        if user:
            serializer.validate_exist_user_email(serializer.initial_data)
            user.confirmation_code = (
                self._get_confirmation_code_and_send_email(user.email)
            )
            user.save()
            headers = super().get_success_headers(serializer.initial_data)
            return Response(serializer.initial_data, status=status.HTTP_200_OK,
                            headers=headers)
        else:
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
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с пользователями."""
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (IsRoleAdmin,)
    filter_backends = (SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с отзывами."""

    serializer_class = serializers.ReviewSerializer
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


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с комментариями."""

    serializer_class = serializers.CommentSerializer
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
    permission_classes = (IsRoleAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ('partial_update', 'create'):
            return serializers.PostPatchTitleSerializer
        return serializers.GetTitleSerializer


class CategoryViewSet(mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    """Вьюсет для работы с категориями."""
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (IsRoleAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    """Вьюсет для работы с жанрами."""
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = (IsRoleAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
