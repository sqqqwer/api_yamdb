from django.core.validators import MaxValueValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from yamdb.constants import (
    STR_OUTPUT_LIMIT,
    NAME_MAX_LENGTH,
    SLUG_MAX_LENGTH
)

ROLES = ('user', 'moderator', 'admin', 'superuser')


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    role = models.CharField(
        max_length=15,
        choices=ROLES
    )
    confirmation_code = models.CharField(max_length=5)
    bio = models.TextField(max_length=511)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return (
            {
                'refresh': str(refresh),
                'refresh': str(refresh.access_token),
            }
        )


class Title(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    year = models.PositiveSmallIntegerField()
    # rating - Определяется на основе отзывов
    description = models.TextField(null=True, blank=True)
    genres = models.ManyToManyField('Genre')
    # category = models.ForeignKey('Category')
    # null=True, blank=False, on_delete=models.SET_NULL) - на будущее
    category = models.ForeignKey(
        'Category',
        null=True, blank=False, on_delete=models.SET_NULL
    )

    class Meta:
        default_related_name = 'titles'
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:STR_OUTPUT_LIMIT]


class Genre(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    slug = models.SlugField(max_length=SLUG_MAX_LENGTH, unique=True)

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:STR_OUTPUT_LIMIT]


class Category(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    slug = models.SlugField(max_length=SLUG_MAX_LENGTH, unique=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:STR_OUTPUT_LIMIT]


class Review(models.Model):
    text = models.TextField(
        'Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва'
    )
    score = models.SmallIntegerField(
        'Оценка пользователя',
        validators=(MaxValueValidator(10),)
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        default_related_name = 'reviews'

    def __str__(self):
        return (
            f'Пользователь: "{self.author}", '
            f'текст отзыва: "{self.text[:STR_OUTPUT_LIMIT]}", '
            f'оценка: "{self.score}".'
        )
