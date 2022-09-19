import base64

from django.db.models import Sum
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination

from recipes.models import IngredientRecipe


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]

            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)

        return super().to_internal_value(data)


class PageNumberWithLimitPagination(PageNumberPagination):
    page_size_query_param = "limit"
    page_size = 5
    max_page_size = 100


def to_txt(recipes):
    ingredient_ids = recipes.values_list("ingredients")
    ingredients = IngredientRecipe.objects.filter(id__in=ingredient_ids)
    ingredients_with_amount = ingredients.values(
        "ingredient__name", "ingredient__measurement_unit"
    ).annotate(total_amount=Sum("amount"))
    pre_result = []
    for ingr in ingredients_with_amount:
        pre_result.append(
            (
                f"{ingr['ingredient__name']} "
                f"{ingr['total_amount']} "
                f"{ingr['ingredient__measurement_unit']}"
            )
        )
    result = "\n".join(pre_result)
    return result
