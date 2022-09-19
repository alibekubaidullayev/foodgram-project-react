from django_filters import rest_framework as filters

from recipes.models import Recipe, Favorite, ShoppingCart


class RecipeFilter(filters.FilterSet):
    author = filters.NumberFilter(field_name="author__pk")
    tags = filters.CharFilter(field_name="tags__slug", lookup_expr="contains")
    is_favorited = filters.BooleanFilter(method="filter_is_favorited")
    is_in_shopping_cart = filters.BooleanFilter(method="filter_in_cart")

    def _fav_shop_filter(self, queryset, model):
        required = model.objects.filter(user=self.request.user)
        required = required.values_list("recipe")
        return queryset.filter(id__in=required)

    def filter_is_favorited(self, queryset, name, value):
        return self._fav_shop_filter(queryset, Favorite)

    def filter_in_cart(self, queryset, name, value):
        return self._fav_shop_filter(queryset, ShoppingCart)

    class Meta:
        model = Recipe
        fields = ["author", "tags", "is_favorited", "is_in_shopping_cart"]


# class IngredientSearchFilter(filters.FilterSet):
    