# Generated by Django 5.0.2 on 2025-03-16 09:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pro", "0013_productimage"),
    ]

    operations = [
        migrations.CreateModel(
            name="ShoeSize",
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
                ("size", models.CharField(max_length=10, unique=True)),
            ],
        ),
    ]
