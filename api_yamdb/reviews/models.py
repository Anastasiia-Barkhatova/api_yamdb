from django.db import models


class Category(models.Model):
    name = models.CharField(
        verbose_name='Заголовок',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Slug категории',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Жанр',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Slug жанра',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Произведение',
        max_length=256,
    )
    year = models.SmallIntegerField(
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
        related_name='categoryes'
    )
    genres = models.ManyToManyField(Genre, related_name='genres')

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'

    def __str__(self):
        return self.name
