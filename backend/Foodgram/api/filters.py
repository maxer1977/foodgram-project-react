import django_filters
from django_filters import CharFilter, rest_framework
from reciepts.models import Ingridients, Reciepts, Tags

from .utility import filter_it


class RecieptsFilterSet(django_filters.FilterSet):
    """Фильтры для списка рецептов."""

    author = django_filters.NumberFilter(
        field_name="author__pk", lookup_expr="exact")
    tags = django_filters.filters.ModelMultipleChoiceFilter(
        queryset=Tags.objects.all(), field_name="tag_list__slug",
        to_field_name="slug"
    )
    is_favorited = django_filters.NumberFilter(method="filter_is_favorited")
    is_in_shopping_cart = django_filters.NumberFilter(
        method="filter_is_in_shopping_cart"
    )

    def filter_is_favorited(self, queryset, name, value):
        param = "favorit__user"
        return filter_it(queryset, self.request, value, param)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        param = "shopping__user"
        return filter_it(queryset, self.request, value, param)

    class Meta:
        model = Reciepts
        fields = ("tags", "author", "is_favorited", "is_in_shopping_cart")


class IngridientListFilterSet(rest_framework.FilterSet):
    """Фильтр-поиск для списка ингредиентов."""

    name = CharFilter(field_name="ingridient", lookup_expr="istartswith")

    class Meta:
        model = Ingridients
        fields = ["name"]
