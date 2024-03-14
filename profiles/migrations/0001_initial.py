# Generated by Django 4.2.3 on 2024-03-06 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Profiles",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("password", models.CharField(max_length=80, unique=True)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
