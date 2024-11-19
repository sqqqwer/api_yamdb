from django.contrib.auth import get_user_model
from django.db import models

from reviews.constants import NAME_MAX_LENGTH, STR_OUTPUT_LIMIT

User = get_user_model()


class AbstractTagModel(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)
    slug = models.SlugField(
        'Человекочитаемый ключ',
        unique=True)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[:STR_OUTPUT_LIMIT]


class AbstractCommentReviewModel(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return f'Автор: {self.author}, Дата: {self.pub_date}'
