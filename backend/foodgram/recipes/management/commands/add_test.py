from pydoc import describe

from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from recipes.models import Ingredient, Recipe, Tag, User

aut = User.objects.create(
    username='a',
    email='a@gmail.com',
    first_name='a',
    last_name='b',
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        i = Ingredient(name='onion', amount=1, unit='шт')
        i.save()
        t = Tag(name='Lunch', hexcolor='1111111', slug='lunch')
        t.save()
        aut = get_object_or_404(User, pk=1)
        r = Recipe(author=aut, name='hui',
                   description='zaebal', cooking_time_m=10)
        r.save()
        r.tags.add(t)
        r.ingredients.add(i)
