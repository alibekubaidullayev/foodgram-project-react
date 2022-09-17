import base64

from django.db.models import Case, Sum, When
from django.core.files.base import ContentFile
from rest_framework import serializers
from recipes.models import Ingredient, IngredientRecipe


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]

            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)

        return super().to_internal_value(data)


def to_txt(recipes):
    ingredient_ids = recipes.values_list("ingredients")
    ingredients = IngredientRecipe.objects.filter(id__in=ingredient_ids)
    ingredients_with_amount = Ingredient.objects.annotate(
        amount=Sum(
            Case(
                When(
                    ingredient_recipe__in=ingredients,
                    then=("ingredient_recipe__amount"),
                )
            )
        )
    )
    pre_result = []
    for ingr in ingredients_with_amount:
        pre_result.append(f"{ingr.name} {ingr.amount} {ingr.measurement_unit}")
    result = '\n'.join(pre_result)
    return result
