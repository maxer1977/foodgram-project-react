import django_filters
from django_filters import rest_framework, CharFilter

from reciepts.models import Tags, Reciepts, Ingridients


class RecieptsFilterSet(django_filters.FilterSet):

    author = django_filters.NumberFilter(field_name='author__pk', lookup_expr='exact')
    tags = django_filters.filters.ModelMultipleChoiceFilter(queryset=Tags.objects.all(), field_name='tag_list__slug', to_field_name='slug')
    is_favorited = django_filters.NumberFilter(method='filter_is_favorited')
    is_in_shopping_cart = django_filters.NumberFilter(method='filter_is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        author = self.request.user
        if author.is_anonymous or value == 0:
            return queryset
        elif value == 1:
            return queryset.filter(favorit__user=author)
    
    def filter_is_in_shopping_cart(self, queryset, name, value):
        author = self.request.user
        if author.is_anonymous or value == 0:
            return queryset
        elif value == 1:
            return queryset.filter(shopping__user=author)

    class Meta:
        model = Reciepts
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']


class IngridientListFilterSet(rest_framework.FilterSet):
    name = CharFilter(field_name='ingridient', lookup_expr='istartswith')

    class Meta:
        model = Ingridients
        fields = ['name']

