from rest_framework.routers import SimpleRouter

from django.urls import include, path

from recipes.views import TagViewSet, IngredientViewSet, RecipeViewSet

app_name = 'api'

router = SimpleRouter()

router.register('tags', TagViewSet)
router.register('ingerdients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 