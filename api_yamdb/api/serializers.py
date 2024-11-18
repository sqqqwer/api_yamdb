from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api_yamdb.settings import FROM_EMAIL
from reviews.constants import (BAN_USERNAME, DEFAULT_TITLE_RATING,
                               EMAIL_MAX_LENGTH, MAX_SCORE_VALUE,
                               MIN_SCORE_VALUE, ROLES, USERNAME_MAX_LENGTH)
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class PostPatchReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с созданием или изменением отзывов."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    score = serializers.IntegerField(
        validators=[MinValueValidator(MIN_SCORE_VALUE),
                    MaxValueValidator(MAX_SCORE_VALUE)]
    )
    text = serializers.CharField()

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, attrs):
        if self.context['request'].method == 'POST':
            if Review.objects.filter(
                author=self.context['request'].user,
                title_id=self.context.get('view').kwargs.get('title_id')
            ).exists():
                raise serializers.ValidationError(
                    'Вы уже оставили отзыв на это произведение.')

        return attrs


class GetReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для получения отзывов."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

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


class GetTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для работы получения данных о произведении."""

    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(
        read_only=True, default=DEFAULT_TITLE_RATING)

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title


class PostPatchTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с созданием или изменением произведений."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        allow_empty=False,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    year = serializers.IntegerField()

    class Meta:
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category')
        model = Title

    def validate_year(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего')
        return value

    def to_representation(self, instance):
        response = GetTitleSerializer().to_representation(instance)
        return response


class RegistrationSerializer(serializers.Serializer):
    """Сериализатор для регистрации."""

    username = serializers.CharField(max_length=USERNAME_MAX_LENGTH,
                                     validators=[UnicodeUsernameValidator()])
    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH)

    class Meta:
        fields = ('username', 'email',)

    def validate_username(self, username):
        if username == BAN_USERNAME:
            raise serializers.ValidationError('Некорректное имя пользователя.')
        return username

    def validate(self, attrs):
        print(attrs['username'])
        user_with_username = User.objects.filter(
            username=attrs['username']).first()
        if user_with_username and user_with_username.email != attrs['email']:
            raise serializers.ValidationError('Некорректная почта.')

        user_with_email = User.objects.filter(
            email=attrs['email']).first()
        if user_with_email and not user_with_username:
            raise serializers.ValidationError('Почта занята.')
        return attrs

    def create(self, validated_data):
        user, is_created = User.objects.get_or_create(**validated_data)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Code of api_yamdb',
            message=confirmation_code,
            from_email=FROM_EMAIL,
            recipient_list=[user.email],
        )
        return user


class TokenSerializer(serializers.Serializer):
    """Сериализатор для работы с токеном."""

    username = serializers.CharField(max_length=USERNAME_MAX_LENGTH,
                                     validators=[UnicodeUsernameValidator()])
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        user = get_object_or_404(User, username=attrs['username'])
        if not default_token_generator.check_token(
            user, attrs['confirmation_code']
        ):
            raise serializers.ValidationError('Неверный код подтверждения.')
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с пользователями."""

    role = serializers.ChoiceField(choices=ROLES, default='user')

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User


class UserMeSerializer(UserSerializer):
    """Сериализатор для получения и редактирования своей учетной записи."""

    role = serializers.ChoiceField(choices=ROLES, read_only=True)

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role',)
        model = User


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с комментариями."""

    author = serializers.SlugRelatedField(
        'username',
        read_only=True,
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
