import datetime

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название произведения', max_length=100)
    year = models.IntegerField(
        'Год публикации',
        default=datetime.date.today().year
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        verbose_name='Категория',
        related_name='titles', blank=True, null=True
    )
    genre = models.ManyToManyField(
        Genre, through='GenreTitle', verbose_name='Жанр'
    )


class GenreTitle(models.Model):
    title_id = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='genres', verbose_name=''
    )
    genre_id = models.ForeignKey(
        Genre, on_delete=models.CASCADE,
        related_name='titles', verbose_name=''
    )

    class Meta:
        verbose_name_plural = 'Жанры'
        constraints = [
            models.UniqueConstraint(
                fields=['title_id', 'genre_id'],
                name='unique_constraint_fail',
            ),
        ]