import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, UserSerializer
from reciepts.models import (IngridientList, Ingridients, Reciepts, Shopping,
                             Subscriptions, Tags)
from rest_framework import serializers

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    """Сериализатор для работы с изображениями."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class CustomUserSerializer(UserSerializer):
    """Сериализатор для отображения информации User."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscriptions.objects.filter(user=user, author=obj.id).exists()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        recipes_limit = int(self.context['request'].GET.get(
            'recipes_limit', 0))
        if recipes_limit:
            representation['recipes'] = representation[
                'recipes'][:recipes_limit]
        return representation


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для записи информации User."""

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'password')


class TagsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Tags."""

    class Meta:
        model = Tags
        fields = ('id', 'name', 'color', 'slug')


class IngridientsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingridients."""

    name = serializers.CharField(source='ingridient')
    measurement_unit = serializers.CharField(source='measure')

    class Meta:
        model = Ingridients
        fields = ('id', 'name', 'measurement_unit')


class IngridientsListSerializer(serializers.ModelSerializer):
    """Сериализатор для модели списка Ingridients."""

    id = serializers.ReadOnlyField(source='ingridient.id')
    name = serializers.ReadOnlyField(source='ingridient.ingridient')
    measurement_unit = serializers.ReadOnlyField(source='ingridient.measure')
    amount = serializers.ReadOnlyField(source='quantity')

    class Meta:
        model = IngridientList
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecieptsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Reciepts."""

    tags = TagsSerializer(many=True, source='tag_list')
    author = CustomUserSerializer(many=False)
    ingredients = IngridientsListSerializer(
        many=True, source='ingridient_lists')
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    name = serializers.CharField(source='title')
    cooking_time = serializers.CharField(source='duration')

    class Meta:
        model = Reciepts
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return obj.favorit.all().exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return obj.shopping.all().exists()


class ShortRecieptsSerializer(serializers.ModelSerializer):
    """Краткий сериализатор для модели Reciepts."""

    name = serializers.CharField(source='title', read_only=True)
    cooking_time = serializers.CharField(source='duration', read_only=True)

    class Meta:
        model = Reciepts
        fields = ('id', 'name', 'image', 'cooking_time')

    def create(self, validated_data):

        user = self.context['request'].user
        recipe = self.context['view'].get_object()
        Shopping.objects.create(user=user, reciept=recipe)
        return recipe


class NewIngridientsListSerializer(serializers.ModelSerializer):
    """Сериализатор для нового списка модели Ingridients."""

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingridients.objects.all(), many=False,
        read_only=False, source='ingridient')
    amount = serializers.IntegerField(min_value=1, source='quantity')

    class Meta:
        model = IngridientList
        fields = ('id', 'amount')


class NewRecieptsSerializer(serializers.ModelSerializer):
    """Сериализатор для нового рецепта Reciepts."""

    ingredients = NewIngridientsListSerializer(
        many=True, source='ingridient_lists')
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tags.objects.all(), source='tag_list')
    image = Base64ImageField()
    name = serializers.CharField(source='title')
    cooking_time = serializers.IntegerField(source='duration', min_value=1)

    class Meta:
        model = Reciepts
        fields = ('ingredients', 'tags', 'image',
                  'name', 'text', 'cooking_time')

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingridient_lists')

        tags_data = validated_data.pop('tag_list')

        validated_data['author'] = self.context['request'].user

        reciept = Reciepts.objects.create(**validated_data)

        for ingridient_data in ingredients_data:
            ingridient = ingridient_data['ingridient']
            IngridientList.objects.create(
                reciept=reciept, ingridient=ingridient,
                quantity=ingridient_data['quantity'])

        reciept.tag_list.set(tags_data)
        return reciept

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)

        if 'tag_list' in validated_data:
            tags_data = validated_data.pop('tag_list')
            print(tags_data)
            instance.tag_list.set(tags_data)

        if 'ingridient_lists' in validated_data:
            ingridients_data = validated_data.pop('ingridient_lists')
            print(ingridients_data)
            IngridientList.objects.filter(reciept=instance).delete()
            for ingridient_data in ingridients_data:
                ingridient = ingridient_data['ingridient']
                reciept = instance
                IngridientList.objects.create(
                    reciept=reciept, ingridient=ingridient,
                    quantity=ingridient_data['quantity'])
        instance.save()
        return instance


class SubscriptionsSerializer(CustomUserSerializer):
    """Сериализатор для подписки Subscriptions."""

    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)
    email = serializers.EmailField(read_only=True)
    username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes_count(self, obj):
        author = obj
        return author.reciepts.count()

    def get_recipes(self, obj):
        author = obj
        # author = self.request.user
        recipes = author.reciepts.all()
        serializer = ShortRecieptsSerializer(recipes, many=True)
        return serializer.data

    def create(self, validated_data):

        user = self.context['request'].user
        author = self.context['view'].get_object()
        subscription = Subscriptions.objects.create(
            user=user, author=author)
        return subscription
