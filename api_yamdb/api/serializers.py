from rest_framework import serializers

from yamdb.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с отзывами."""

    # author = serializers.SlugRelatedField(
    #     'username',
    #     read_only=True
    # )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
