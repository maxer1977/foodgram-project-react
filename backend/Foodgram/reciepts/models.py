from django.db import models

from users.models import User


class Ingridients(models.Model):
    """Модель для коллекции ингридиентов."""

    ingridient = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Название продукта')
    measure = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Единица измерения')
    
    class Meta:
        verbose_name_plural = 'Ингридиенты'
        verbose_name = 'Ингридиент'

    def __str__(self):
        return self.ingridient[:20]

class Tags(models.Model):
    """Модель для тэгов."""

    name = models.CharField(
        max_length=50,
        blank=True,
        unique=True,
        verbose_name='Название тэга')
    color = models.CharField(
        max_length=16,
        blank=True,
        unique=True,
        verbose_name='Цвет тэга')
    slug = models.SlugField(unique=True, max_length=20)
    
    class Meta:
        verbose_name_plural = 'Тэги'
        verbose_name = 'Тэг'

    def __str__(self):
        return self.name[:20]


class Reciepts(models.Model):
    """Модель для рецептов пользователей."""

    author = models.ForeignKey(
        User,
        related_name='reciepts',
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта')

    title = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Название рецепта')

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации рецепта')

    text = models.TextField(verbose_name='Описание рецепта')

    duration = models.PositiveSmallIntegerField(
        verbose_name='Длительность приготовления в минутах')

    image = models.ImageField(
        upload_to='images/',
        null=True,
        default=None
        )

    ingridients_list = models.ManyToManyField(
        Ingridients,
        related_name='reciepts',
        verbose_name='Список ингридиентов',
        blank=True)

    tag_list = models.ManyToManyField(
        Tags,
        related_name='reciepts',
        verbose_name='Список тэгов',
        blank=True)

    class Meta:
        verbose_name_plural = 'Рецепты'
        verbose_name = 'Рецепт'

    def __str__(self):
        return self.title[:20]