# Generated by Django 4.1 on 2022-09-09 06:11

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("recipes", "0004_favourite"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Favourite",
            new_name="Favorite",
        ),
    ]