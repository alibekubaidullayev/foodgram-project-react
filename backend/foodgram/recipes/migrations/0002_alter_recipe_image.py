# Generated by Django 4.1 on 2022-09-07 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="image",
            field=models.ImageField(
                blank=True, upload_to="../../tmp_media", verbose_name="Image"
            ),
        ),
    ]