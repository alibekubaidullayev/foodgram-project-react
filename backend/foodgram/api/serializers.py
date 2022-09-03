import base64
import datetime as dt


from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import Ingredient, Recipe, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'hexcolor', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = ('name', 'amount', 'unit')


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Recipe
        # read_only_fields = ('__all__',)
        fields = ('author', 'name', 'description',
                  'ingredients', 'tags', 'cooking_time_m')

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        
