# Generated by Django 4.1.5 on 2023-02-04 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0002_travelogue_is_approved_vehicle_is_approved_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vehicle",
            name="description",
            field=models.TextField(max_length=2000),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="feature",
            field=models.TextField(max_length=1000),
        ),
    ]