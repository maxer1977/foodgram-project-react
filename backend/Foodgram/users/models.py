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
        blank=False,
        null=False,
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
        message='Пароль состоит только букв и цифрв. Должно быть хотя бы одна буква и одна цифра (не менее 8 символов)',
    )
    password = models.CharField(
        validators=[password_validator],
        max_length=150,
        blank=False,
        null=False,
        verbose_name='Пароль пользователя'
        )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
