from tabnanny import verbose
from django.contrib.auth.models import AbstractUser
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models

from .validators import year_validator


class User(AbstractUser):

    USERS_ROLES = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    )

    username = models.CharField(
        unique=True, max_length=150, verbose_name='Имя пользователя',
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message=(
                    'Username may only consist of letters,',
                    'digits and @/./+/-/_'
                ),
            ),
        ]
    )
    email = models.EmailField(
        unique=True, verbose_name='Электронная почта'
    )
    first_name = models.CharField(
        max_length=150, blank=True, verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=150, blank=True, verbose_name='Фамилия'
    )
    bio = models.TextField(
        blank=True, verbose_name='О себе'
    )
    role = models.CharField(
        max_length=50, choices=USERS_ROLES, default='user', verbose_name='Роль'
    )

    class Meta:
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(
        max_length=256, verbose_name='Название категории'
    )
    slug = models.SlugField(
        max_length=50, unique=True, verbose_name='Слаг категории'
    )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256, verbose_name='Название жанра'
    )
    slug = models.SlugField(
        max_length=50, unique=True, verbose_name='Слаг жанра'
    )

    class Meta:
        verbose_name = 'Genre',
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=100, verbose_name='Название произведения'
        )
    year = models.IntegerField(
        validators=[year_validator,],
        verbose_name='Год публикации'
    )
    description = models.TextField(
        blank=True, verbose_name='Описание произведения'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', blank=True, null=True,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre, through='GenreTitle',
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Title',
        verbose_name_plural = 'Titles'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='genres', verbose_name='Произведение'
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE,
        related_name='titles', verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Title Genre'
        verbose_name_plural = 'Title Genres'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'],
                name='unique_constraint_fail',
            ),
        ]


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(1, "Оценка не может быть ниже '1'."),
            MaxValueValidator(10, "Оценка не может быть выше '10'.")
        ],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review_constaint')
        ]

    def __str__(self):
        return self.text[:50]


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Сomments'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
