# Generated by Django 5.0.2 on 2025-03-16 11:22

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("pro", "0015_product_sizes"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="sizes",
        ),
        migrations.DeleteModel(
            name="ShoeSize",
        ),
    ]
