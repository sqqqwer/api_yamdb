from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.abstracts import AbstractCommentReviewModel, AbstractTagModel
from reviews.constants import (DEFAULT_ROLE, EMAIL_MAX_LENGTH, MAX_SCORE_VALUE,
                               MIN_SCORE_VALUE, NAME_MAX_LENGTH,
                               PASSWORD_MAX_LENGTH, ROLE_ADMIN, ROLE_INDEX,
                               ROLE_MODERATOR, ROLES, STR_OUTPUT_LIMIT)
from reviews.validators import validate_year


class User(AbstractUser):
    max_role_length = max(len(role[ROLE_INDEX]) for role in ROLES)
    password = models.CharField(
        blank=True,
        null=True,
        max_length=PASSWORD_MAX_LENGTH
    )
    email = models.EmailField('Почта',
                              unique=True,
                              max_length=EMAIL_MAX_LENGTH)
    role = models.CharField('Роль', choices=ROLES,
                            max_length=max_role_length,
                            default=DEFAULT_ROLE)
    bio = models.TextField(
        'Биография',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return f'{self.username}-{self.role} - {self.email}'

    @property
    def is_admin(self):
        return self.role == ROLE_ADMIN

    @property
    def is_moderator(self):
        return self.role == ROLE_MODERATOR


class Genre(AbstractTagModel):

    class Meta(AbstractTagModel.Meta):
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Category(AbstractTagModel):

    class Meta(AbstractTagModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)
    year = models.SmallIntegerField(
        'Год выпуска',
        validators=(validate_year,)
    )
    description = models.TextField('Описание', null=True, blank=True)
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        null=True, on_delete=models.SET_NULL,
        verbose_name='Категория'
    )

    class Meta:
        default_related_name = 'titles'
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year',)

    def __str__(self):
        return self.name[:STR_OUTPUT_LIMIT]


class Review(AbstractCommentReviewModel):
    score = models.PositiveSmallIntegerField(
        'Оценка пользователя',
        validators=[MinValueValidator(MIN_SCORE_VALUE),
                    MaxValueValidator(MAX_SCORE_VALUE)]
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )

    class Meta(AbstractCommentReviewModel.Meta):
        default_related_name = 'reviews'
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='unique_review'
                                    )
        ]

    def __str__(self):
        return (
            f'Пользователь: "{self.author}", '
            f'текст отзыва: "{self.text[:STR_OUTPUT_LIMIT]}", '
            f'оценка: "{self.score}".'
        )


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, null=True, on_delete=models.SET_NULL)
    genre = models.ForeignKey(Genre, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ('title',)


class Comment(AbstractCommentReviewModel):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )

    class Meta(AbstractCommentReviewModel.Meta):
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'

    def __str__(self):
        return (
            f'Пользователь: "{self.author}", '
            f'Текст комментария : "{self.text[:STR_OUTPUT_LIMIT]}".'
        )
