from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


class Review(models.Model):
    text = models.TextField('Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    # title = models.ForeignKey(
    #     Title,
    #     on_delete=models.CASCADE,
    #     related_name='reviews',
    #     verbose_name='Произведение',
    # )
    score = models.PositiveBigIntegerField(
        'Оценка',
        validators=[
            MinValueValidator(1, message='Установите значение от 1 до 10'),
            MaxValueValidator(10, message='Установите значение от 1 до 10'),
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_author_title'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField('Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
        related_name='comments'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
