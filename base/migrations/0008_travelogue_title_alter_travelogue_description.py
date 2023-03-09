# Generated by Django 4.1.5 on 2023-03-04 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0007_raterent_delete_ratevehicle"),
    ]

    operations = [
        migrations.AddField(
            model_name="travelogue",
            name="title",
            field=models.CharField(default="Default Title", max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="travelogue",
            name="description",
            field=models.CharField(max_length=4000),
        ),
    ]
