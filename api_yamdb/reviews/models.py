from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from reviews.constants import MAX_SCORE, MIN_SCORE, NAME_LENGHT, TEXT_LENGTH
from reviews.validates import validate_year

User = get_user_model()


class CommonCategoryGenreModel(models.Model):
    """Абстрактная модель для категорий и жанров."""

    name = models.CharField(max_length=NAME_LENGHT, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Slug')

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[:TEXT_LENGTH]


class Category(CommonCategoryGenreModel):
    """Модель категорий."""

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Genre(CommonCategoryGenreModel):
    """Модель жанров."""

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField(
        verbose_name='Произведение',
        max_length=NAME_LENGHT,
    )
    year = models.SmallIntegerField(
        validators=(validate_year,),
        verbose_name='Год выпуска',
        db_index=True
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'
        default_related_name = 'titles'
        ordering = ('name',)

    def __str__(self):
        return self.name


class CommonReviewCommentModel(models.Model):
    """Абстрактная модель для обзоров и комментариев."""

    text = models.TextField('Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:TEXT_LENGTH]


class Review(CommonReviewCommentModel):
    """Модель отзывов."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    score = models.SmallIntegerField(
        'Оценка',
        null=True,
        validators=[
            MinValueValidator(MIN_SCORE),
            MaxValueValidator(MAX_SCORE)
        ],
        help_text=f'Установите значение от {MIN_SCORE} до {MAX_SCORE}'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_author_title'
            )
        ]


class Comment(CommonReviewCommentModel):
    """Модель комментариев."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
        related_name='comments'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
