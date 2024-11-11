from django.core.validators import MaxValueValidator
from django.db import models

from yamdb.constants import TEXT_LENGTH


class Review(models.Model):
    text = models.TextField(
        'Текст отзыва'
    )
    # Ниже заглушка пока модели пользователя нет
    # author = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     verbose_name='Автор отзыва'
    # )
    author = models.SmallIntegerField()
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
            f'текст отзыва: "{self.text[:TEXT_LENGTH]}", '
            f'оценка: "{self.score}".'

        )
