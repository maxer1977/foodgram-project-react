import csv
from io import StringIO

from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from reciepts.models import (Favorits, IngridientList, Ingridients, Reciepts,
                             Shopping, Subscriptions, Tags)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import User

from .filters import IngridientListFilterSet, RecieptsFilterSet
from .paginator import CustomPaginator
from .permissions import IsAuthorOrReadOnly
from .serializers import (CustomUserSerializer, IngridientsListSerializer,
                          IngridientsSerializer, NewRecieptsSerializer,
                          RecieptsSerializer, ShortRecieptsSerializer,
                          SubscriptionsSerializer, TagsSerializer)


class TagsViewSet(viewsets.ModelViewSet):
    """ViewSet для получения информации о Тэгах."""

    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get']
    pagination_class = None


class IngridientsViewSet(viewsets.ModelViewSet):
    """ViewSet для получения информации о Ingridients."""

    queryset = Ingridients.objects.all()
    serializer_class = IngridientsSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get']
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngridientListFilterSet


class IngridientsListViewSet(viewsets.ModelViewSet):
    """ViewSet для получения информации о списке IngridientsList."""

    queryset = IngridientList.objects.all()
    serializer_class = IngridientsListSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get']
    pagination_class = None


class RecieptsViewSet(viewsets.ModelViewSet):
    """ViewSet для получения информации о Reciepts."""

    queryset = Reciepts.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = CustomPaginator
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecieptsFilterSet

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-pub_date')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecieptsSerializer
        elif self.request.method == 'POST' or self.request.method == 'PATCH':
            return NewRecieptsSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
        url_path='favorite',
        url_name='favorite',
    )
    def make_favorite(self, request, pk=None):
        """Работа с Избранным."""

        serializer = ShortRecieptsSerializer(
            data=request.data, context={'request': request, 'view': self})

        recipe_id = self.kwargs['pk']
        recipe = get_object_or_404(Reciepts, pk=recipe_id)

        user = self.request.user

        if request.method == 'POST':

            if not Favorits.objects.filter(
                    reciept=recipe, user=user).exists():
                serializer.is_valid(raise_exception=True)
                serializer.save(reciept=recipe, user=user)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)

            return Response('Этот рецепт уже есть в Вашем избранном!',
                            status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            favorite = get_object_or_404(Favorits, reciept=recipe, user=user)
            favorite.delete()
            return Response('Рецепт удален из избранного!',
                            status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
        url_path='shopping_cart',
        url_name='shopping_cart',
    )
    def edit_shopping(self, request, pk=None):
        """Работа со списком покупок."""

        serializer = ShortRecieptsSerializer(
            data=request.data, context={'request': request, 'view': self})

        recipe_id = self.kwargs['pk']
        recipe = get_object_or_404(Reciepts, pk=recipe_id)

        user = self.request.user

        if request.method == 'POST':
            if not Shopping.objects.filter(
                    reciept=recipe, user=user).exists():
                serializer.is_valid(raise_exception=True)
                print(serializer.validated_data)
                serializer.save(reciept=recipe, user=user)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)

            return Response('Этот рецепт уже добавлен в список покупок!',
                            status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            shopping = get_object_or_404(Shopping, reciept=recipe, user=user)
            shopping.delete()
            return Response('Рецепт удален из списка покупок!',
                            status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
        url_path='download_shopping_cart',
        url_name='download_shopping_cart',
    )
    def download(self, request):
        """Формирование и запись списка покупок."""

        ingredients = IngridientList.objects.filter(
            reciept__shopping__user=request.user
        ).values(
            'ingridient__ingridient',
            'ingridient__measure'
        ).annotate(total=Sum('quantity'))

        output = StringIO()
        writer = csv.writer(output, delimiter='\t')

        writer.writerow(['Список покупок'])
        writer.writerow(['N', 'Название ингредиента',
                         'Единица измерения', 'Сумма'])
        n = 1
        for ingredient in ingredients:
            writer.writerow(
                [str(n).ljust(3),
                 ingredient['ingridient__ingridient'].ljust(20),
                 ingredient['ingridient__measure'].ljust(20),
                 str(ingredient['total']).ljust(3)])
            n = n + 1
        file_contents = output.getvalue()

        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename="ingredients.txt"')
        response.write(file_contents)
        return response


class CustomUserViewSet(UserViewSet):
    """Кастомный ViewSet для User."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPaginator

    @action(
        detail=False,
        methods=('get',),
        permission_classes=[AllowAny],
        url_path='subscriptions',
        url_name='subscriptions',
    )
    def subscriptions(self, request):
        """Список подписок"""

        authors = User.objects.filter(following__user=self.request.user)
        if authors:
            serializer = SubscriptionsSerializer(
                many=True, data=authors, context={'request': request})
            serializer.is_valid()
            return Response(serializer.data)
        return Response('Нет подписок!',
                        status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[AllowAny],
        url_path='subscribe',
        url_name='subscribe',
    )
    def subscribe(self, request, id=None):
        """Работа с подписками."""

        serializer = SubscriptionsSerializer(
            data=request.data, context={'request': request, 'view': self})

        author_id = self.kwargs['id']
        author = get_object_or_404(User, pk=author_id)

        user = self.request.user

        if request.method == 'POST':
            if user == author:
                return Response('Нельзя подписаться на себя!!',
                                status=status.HTTP_400_BAD_REQUEST)

            if not Subscriptions.objects.filter(
                    author=author, user=user).exists():
                serializer.is_valid(raise_exception=True)
                serializer.save(author=author, user=user)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response('Автор уже пристутствует в подписке!',
                            status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            subscription = get_object_or_404(
                Subscriptions, author=author, user=user)
            subscription.delete()
            return Response('Подписка успешно удалена!',
                            status=status.HTTP_204_NO_CONTENT)
