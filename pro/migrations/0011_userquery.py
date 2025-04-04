# Generated by Django 5.0.2 on 2025-03-10 19:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pro", "0010_product_new_product"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserQuery",
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
                ("name", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=254)),
                ("question", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
