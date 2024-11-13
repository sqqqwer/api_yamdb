from rest_framework import viewsets
from yamdb.models import Title
from api.serializers import ReviewSerializer
from api.permissions import IsAuthorOrReadOnly
from django.shortcuts import get_object_or_404


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
        title = self.reviews.all()
        serializer.save(author=self.request.user, title=title)
