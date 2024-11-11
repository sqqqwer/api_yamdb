from django.contrib.auth import get_user_model
from django.db import models

from posts.constants import (
    STR_OUTPUT_LIMIT,
    NAME_MAX_LENGTH,
    SLUG_MAX_LENGTH
)


User = get_user_model()


class Title(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    year = models.PositiveSmallIntegerField()
    # rating - Определяется на основе отзывов
    description = models.TextField(null=True, blank=True)
    genres = models.ManyToManyField('Genre')
    category = models.ForeignKey('Category')
    # null=True, blank=False, on_delete=models.SET_NULL) - на будущее

    class Meta:
        default_related_name = 'titles'
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.title[:STR_OUTPUT_LIMIT]


class Genre(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    slug = models.SlugField(max_length=SLUG_MAX_LENGTH, unique=True)

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.title[:STR_OUTPUT_LIMIT]


class Category(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    slug = models.SlugField(max_length=SLUG_MAX_LENGTH, unique=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:STR_OUTPUT_LIMIT]
