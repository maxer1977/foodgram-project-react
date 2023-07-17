# Generated by Django 3.2 on 2023-07-08 15:04

import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Электронная почта')),
                ('username', models.CharField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator(message='Можно использовать ТОЛЬКО буквенно-цифровые символы, а так же точку, собаку, плюс и дефис', regex='^[\\w.@+-]+$')], verbose_name='Сетевое имя пользователя')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='Имя пользователя')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='Фамилия пользователя')),
                ('password', models.CharField(max_length=150, validators=[django.core.validators.RegexValidator(message='Пароль состоит только букв и цифрв. Должно быть хотя бы одна буква и одна цифра (не менее 8 символов)', regex='^(?=.*[A-Za-z])(?=.*\\d)[A-Za-z\\d]{8,}$')], verbose_name='Пароль пользователя')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
