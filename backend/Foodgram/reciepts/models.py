from django.db import models

from users.models import User

from django.core.validators import MaxValueValidator, MinValueValidator


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

    tag_list = models.ManyToManyField(
        Tags,
        related_name='reciepts',
        verbose_name='Список тэгов',
        blank=True)

    ingridients_list = models.ManyToManyField(
        Ingridients,
        through='IngridientList',
        related_name='reciepts',
        verbose_name='Список продуктов',
        blank=True
    )

    class Meta:
        verbose_name_plural = 'Рецепты'
        verbose_name = 'Рецепт'

    def __str__(self):
        return self.title[:20]


class Subscriptions(models.Model):
    """Модель для подписок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='following',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='not_unique_subscription')
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return (f'Автор {self.author.get_username} '
                f'- подписчик {self.user.get_username}')


class Favorits(models.Model):
    """Модель для избранных рецептов."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='favorits',
    )
    reciept = models.ForeignKey(
        Reciepts,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorit',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'reciept'],
                                    name='not_unique_favorit')
        ]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'

    def __str__(self):
        return (f'Пользователь {self.user.get_username} '
                f'- рецепт {self.reciept.title}')


class Shopping(models.Model):
    """Модель для списка покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='shopper',
    )
    reciept = models.ForeignKey(
        Reciepts,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='shopping',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'reciept'],
                                    name='not_unique_shopping_list')
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return (f'Покупатель {self.user.get_username} '
                f'- рецепт {self.reciept.title}')


class IngridientList(models.Model):
    """Модель для указания количества ингредиентов."""

    reciept = models.ForeignKey(
        Reciepts,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='ingridient_lists',
    )

    ingridient = models.ForeignKey(
        Ingridients,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент',
        related_name='ingridients',
    )

    quantity = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1)
        ],
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Список ингридиентов'
        verbose_name_plural = 'Списки ингридиентов'

    def __str__(self):
        return (f'Рецепт - {self.ingridient.ingridient}')

