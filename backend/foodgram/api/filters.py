from django_filters import rest_framework as filters

from recipes.models import Recipe


class RecipeFilter(filters.FilterSet):
    author = filters.NumberFilter(field_name="author__pk", lookup_expr="contains")
    tags = filters.CharFilter(field_name="tags__slug", lookup_expr="contains")

    class Meta:
        model = Recipe
        fields = [
            "author",
            "tags",
        ]
