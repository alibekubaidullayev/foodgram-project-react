from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from recipes.models import Ingredient, Recipe, Tag, Favorite


from .filters import RecipeFilter
from .serializers import (
    IngredientSerializer,
    RecipeSerializer,
    RecipeCreateSerializer,
    TagSerializer,
)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        return (
            RecipeSerializer
            if self.action in ("list", "retrieve")
            else RecipeCreateSerializer
        )

    @action(methods=['POST', 'DELETE'], detail=True)
    def favorite(self, request, *args, **kwargs):
        user = request.user
        recipe = self.get_object()
        if request.method == 'POST':
            Favorite.objects.create(user=user, recipe=recipe)
            return Response(status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            favorite = Favorite.objects.filter(user=user, recipe=recipe)
            favorite.delete()
            return Response(status=status.HTTP_200_OK)

    def perform_update(self, serializer, pk=None):
        instance = self.get_object()
        if self.request.user.is_authenticated:
            updated_instance = serializer.save(author=self.request.user)
        else:
            updated_instance = serializer.save()