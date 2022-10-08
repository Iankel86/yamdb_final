from django.core.validators import RegexValidator
from django.db import models

from titles.validators import year_validator


class Category(models.Model):
    """Категории произведений."""
    name = models.CharField(max_length=256, verbose_name='Название категории')
    slug = models.SlugField(
        max_length=50,
        verbose_name='slug',
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Недопустимый символ в slug категории.'
        )])

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        indexes = [
            models.Index(fields=['name', ]),
        ]

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанры произведений."""
    name = models.CharField(max_length=256, verbose_name='Название жанра')
    slug = models.SlugField(max_length=50, unique=True,
                            verbose_name='Slug жанра')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        indexes = [
            models.Index(fields=['name', ]),
        ]

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения."""
    name = models.CharField(max_length=500, verbose_name='Название')
    year = models.PositiveIntegerField(
        verbose_name='Год выпуска',
        validators=[year_validator]
    )
    description = models.TextField(verbose_name='Описание',
                                   blank=True,
                                   null=True)
    category = models.ForeignKey(Category,
                                 related_name='titles',
                                 on_delete=models.SET_NULL,
                                 blank=True,
                                 null=True,
                                 verbose_name='Категория произведения')
    genre = models.ManyToManyField(Genre,
                                   related_name='titles',
                                   blank=True,
                                   verbose_name='Жанр произведения',
                                   )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
