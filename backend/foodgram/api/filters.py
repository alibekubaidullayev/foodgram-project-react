from django_filters import rest_framework as filters
from recipes.models import Recipe


class RecipeFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='contains'
    )
    ingredients = filters.CharFilter(
        field_name='ingredients__slug',
        lookup_expr='contains'
    )
    tags = filters.CharFilter(
        field_name='tags__slug',
        lookup_expr='contains'
    )

    class Meta:
        model = Recipe
        fields = ['name', 'ingredients', 'tags']
