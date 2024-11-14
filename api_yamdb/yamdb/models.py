from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MaxLengthValidator, MaxValueValidator, MinValueValidator
)
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from yamdb.constants import (
    STR_OUTPUT_LIMIT,
    NAME_MAX_LENGTH,
    ROLES
)
from yamdb.abstracts import AbstractTagModel
from yamdb.constants import NAME_MAX_LENGTH, STR_OUTPUT_LIMIT


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    role = models.CharField(
        max_length=15,
        choices=ROLES
    )
    confirmation_code = models.CharField(max_length=5)
    bio = models.TextField(max_length=511)

    # это вроде не нужно же?
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return (
            {
                'refresh': str(refresh),
                'refresh': str(refresh.access_token),
            }
        )


class Title(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        validators=(
            MaxValueValidator(datetime.now().year),
            MaxLengthValidator(4)
        )
    )
    # rating - Определяется на основе отзывов
    description = models.TextField('Описание', null=True, blank=True)
    genre = models.ManyToManyField(
        'Genre',
        through='TitleGenre',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        'Category',
        null=True, blank=False, on_delete=models.SET_NULL,
        verbose_name='Категория'
    )

    class Meta:
        default_related_name = 'titles'
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:STR_OUTPUT_LIMIT]


class Genre(AbstractTagModel):

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Category(AbstractTagModel):

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


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
        validators=[MinValueValidator(1), MaxValueValidator(10),]
    )
    pub_date = models.DateTimeField(
        'Дата добавления отзыва',
        auto_now_add=True,
        db_index=True
    )
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )

    class Meta:
        default_related_name = 'reviews'

    def __str__(self):
        return (
            f'Пользователь: "{self.author}", '
            f'текст отзыва: "{self.text[:STR_OUTPUT_LIMIT]}", '
            f'оценка: "{self.score}".'
        )


class TitleGenre(models.Model):
    title = models.ForeignKey('Title', null=True, on_delete=models.SET_NULL)
    genre = models.ForeignKey('Genre', null=True, on_delete=models.SET_NULL)


class Comment(models.Model):
    text = models.TextField(
        'Текст комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        'Дата добавления комментария',
        auto_now_add=True,
        db_index=True
    )
    review = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )

    class Meta:
        default_related_name = 'comments'

    def __str__(self):
        return (
            f'Пользователь: "{self.author}", '
            f'Текст комментария : "{self.text[:STR_OUTPUT_LIMIT]}".'
        )
