from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from api.permissions import IsAuthorOrReadOnly
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, GetTitleSerializer,
                             PostPatchTitleSerializer, ReviewSerializer)
from yamdb.models import Category, Genre, Review, Title


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
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')

    def get_serializer_class(self):
        if self.action in ('update', 'create'):
            return PostPatchTitleSerializer
        return GetTitleSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с категориями."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с жанрами."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
