# Generated by Django 4.2.3 on 2024-03-06 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Country",
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
                ("country_name", models.CharField(max_length=60, unique=True)),
                (
                    "continent",
                    models.CharField(
                        choices=[
                            ("AF", "Africa"),
                            ("AN", "Antarctica"),
                            ("AS", "Asia"),
                            ("EU", "Europe"),
                            ("NA", "North America"),
                            ("OC", "Oceania"),
                            ("SA", "South and Central America"),
                        ],
                        max_length=2,
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Language",
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
                ("language", models.CharField(max_length=180)),
                ("language_code", models.CharField(max_length=10)),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="languages",
                        to="qwik_aids.country",
                    ),
                ),
            ],
        ),
    ]
