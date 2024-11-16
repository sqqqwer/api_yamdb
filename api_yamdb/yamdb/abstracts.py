from django.db import models

from yamdb.constants import (
    STR_OUTPUT_LIMIT,
    NAME_MAX_LENGTH,
    SLUG_MAX_LENGTH
)


class AbstractTagModel(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)
    slug = models.SlugField(
        'Человекочитаемый ключ',
        max_length=SLUG_MAX_LENGTH,
        unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:STR_OUTPUT_LIMIT]
