from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg

from yamdb.abstracts import AbstractTagModel
from yamdb.constants import (
    STR_OUTPUT_LIMIT,
    NAME_MAX_LENGTH,
    ROLES
)


class User(AbstractUser):
    password = models.CharField(blank=True, null=True, max_length=128)
    email = models.EmailField('Почта', unique=True)
    role = models.CharField('Роль', choices=ROLES,
                            max_length=10, default='user')
    confirmation_code = models.CharField(max_length=40)
    bio = models.TextField('Биография', blank=True, null=True)

    class Meta:
        default_related_name = 'users'
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username}-{self.role} - {self.email}'


class Title(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        validators=(MaxValueValidator(datetime.now().year), )
    )
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

    @property
    def rating(self):
        rating = self.reviews.aggregate(Avg('score'))['score_avg']
        return int(rating) if rating else 0


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
