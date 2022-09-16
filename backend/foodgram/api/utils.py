import base64

from django.core.files.base import ContentFile

from rest_framework import serializers

from recipes.models import IngredientRecipe


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]

            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)

        return super().to_internal_value(data)


def toTxt(recipes):
    result = ""
    for recipe in recipes:
        ingredient_objs = IngredientRecipe.objects.filter(recipe=recipe)
        ingredients = "Ингредиенты: "
        first = True
        for ingredient in ingredient_objs:
            if not first:
                ingredients += ", "
            else:
                first = False
            ingredients += f"{ingredient.ingredient.name} "
            ingredients += f"{ingredient.amount} "
            ingredients += f"{ingredient.ingredient.measurement_unit}"
        ingredients += ""

        data = [
            f"Название: {recipe.name}",
            ingredients,
            f"Описание: {recipe.text}",
            f"Время приготовления: {recipe.cooking_time}",
        ]
        result += "\n".join(data)
    return result
