# Generated by Django 4.1 on 2022-09-17 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0007_alter_customuser_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="role",
            field=models.CharField(
                choices=[("user", "User"), ("admin", "Administrator")],
                default="user",
                max_length=5,
                verbose_name="Роль",
            ),
        ),
    ]
