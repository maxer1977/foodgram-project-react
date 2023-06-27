from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    """Модель представляющая пользователя."""

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта'
    )

    username_validator = RegexValidator(regex=r'^[\w.@+-]+$', message='Можно использовать ТОЛЬКО буквенно-цифровые символы, а так же точку, собаку, плюс и дефис')
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
        verbose_name='Сетевое имя пользователя'
    )

    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя пользователя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия пользователя'
    )

    password_validator = RegexValidator(
        regex=r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
        message='Пароль должен содержать хотя бы одну букву и одну цифру и быть не менее 8 символов',
    )
    password = models.CharField(
        validators=[password_validator],
        max_length=150,
        verbose_name='Пароль пользователя'
        )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
