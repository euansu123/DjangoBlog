# Generated by Django 5.0.7 on 2025-05-28 08:09

import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ArticlePost",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("body", models.TextField()),
                ("created", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
            ],
            options={
                "ordering": ("-created",),
            },
        ),
        migrations.CreateModel(
            name="ArticleTag",
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
                ("name", models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=100, unique=True)),
                ("icon", models.ImageField(blank=True, upload_to="category")),
                ("description", models.TextField(blank=True, max_length=500)),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
