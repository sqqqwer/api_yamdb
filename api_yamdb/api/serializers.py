from datetime import datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers

from yamdb.models import (
    Category,
    Genre,
    Review,
    Title,
)

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с отзывами."""

    # author = serializers.SlugRelatedField(
    #     'username',
    #     read_only=True
    # )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с жанрами."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для работы с категориями."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class PostPatchTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с созданием или изменением произведений."""

    genre = serializers.SlugRelatedField(
        slug_field='name',
        many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = ('name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title

    def validate_year(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего')
        return value


class GetTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для работы получения данных о произведении."""

    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title


class EmailValidationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError('Who "me"?')
        return username


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)
