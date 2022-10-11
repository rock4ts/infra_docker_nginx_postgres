from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    USERS_ROLES = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    )

    username = models.CharField(
        unique=True,
        max_length=150,
        verbose_name='Имя пользователя',
        help_text='Введите имя пользователя'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Электронная почта',
        help_text='Введите адрес электронной почты'
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя',
        help_text='Введите имя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия',
        help_text='Введите фамилию'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография',
        help_text='Введите биографию'
    )
    role = models.CharField(
        max_length=50,
        choices=USERS_ROLES,
        default='user',
        verbose_name='Роль',
        help_text='Укажите роль пользователя'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
