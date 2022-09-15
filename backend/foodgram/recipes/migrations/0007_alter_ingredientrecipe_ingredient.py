# Generated by Django 4.1 on 2022-09-15 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0006_favorite_unique_favorite_follow_unique_follow_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ingredientrecipe",
            name="ingredient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ingredient",
                to="recipes.ingredient",
                verbose_name="Ингредиент",
            ),
        ),
    ]
