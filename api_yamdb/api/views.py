import random
import string

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, mixins
from rest_framework.permissions import AND, IsAuthenticated, AllowAny
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import IsAuthorOrReadOnly, IsRoleAdmin, IsRoleModerator, IsRoleAdminOrReadOnly
from api import serializers
from yamdb.models import Category, Genre, Review, Title


User = get_user_model()


class RegistrationView(CreateAPIView):
    """APIview для создания пользователя."""
    queryset = User.objects.all()
    serializer_class = serializers.RegistrationSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        confirmation_code = ''.join([random.choice(string.ascii_letters)
                                     for _ in range(40)])
        msg = EmailMultiAlternatives(
            "Code of api_yamdb",
            confirmation_code,
            "from@example.com",
            [serializer.data['email']],
        )
        msg.send()
        serializer.save(confirmation_code=confirmation_code)


class TokenView(CreateAPIView):
    """APIview для получения токена."""
    serializer_class = serializers.TokenSerializer
    '''
    def post(self, request, *args, **kwargs):
        serializer = serializers.TokenReturnSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            refresh.payload.update({  # Полезная информация в самом токене
                'user_id': user.id,
                'username': user.username
            })
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
    '''
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, self.request.user)
        token = str(RefreshToken.for_user(user).access_token)
        serializer = serializers.TokenReturnSerializer(token=token)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserMeView(RetrieveUpdateAPIView):
    """APIview для получения и редактирования своей учетной записи."""

    def get_queryset(self):
        return self.request.user

    def get_serializer_class(self):
        if self.action in ('update'):
            return serializers.UpdateSelfUserSerializer
        return serializers.UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с пользователями."""
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (IsRoleAdmin,)
    lookup_field = 'username'


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
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')

    def get_serializer_class(self):
        if self.action in ('update', 'create'):
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
