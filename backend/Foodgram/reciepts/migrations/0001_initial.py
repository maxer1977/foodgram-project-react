# Generated by Django 3.2 on 2023-07-08 15:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favorits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранные',
            },
        ),
        migrations.CreateModel(
            name='IngridientList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество')),
            ],
            options={
                'verbose_name': 'Список ингридиентов',
                'verbose_name_plural': 'Списки ингридиентов',
            },
        ),
        migrations.CreateModel(
            name='Ingridients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingridient', models.CharField(blank=True, max_length=150, verbose_name='Название продукта')),
                ('measure', models.CharField(blank=True, max_length=100, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'Ингридиент',
                'verbose_name_plural': 'Ингридиенты',
            },
        ),
        migrations.CreateModel(
            name='Reciepts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=150, verbose_name='Название рецепта')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации рецепта')),
                ('text', models.TextField(verbose_name='Описание рецепта')),
                ('duration', models.PositiveSmallIntegerField(verbose_name='Длительность приготовления в минутах')),
                ('image', models.ImageField(default=None, null=True, upload_to='images/')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
            },
        ),
        migrations.CreateModel(
            name='Shopping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Список покупок',
                'verbose_name_plural': 'Списки покупок',
            },
        ),
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, unique=True, verbose_name='Название тэга')),
                ('color', models.CharField(blank=True, max_length=16, unique=True, verbose_name='Цвет тэга')),
                ('slug', models.SlugField(max_length=20, unique=True)),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'Тэги',
            },
        ),
    ]
