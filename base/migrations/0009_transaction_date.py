# Generated by Django 4.1.5 on 2023-03-30 04:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0008_privacypolicy_termsandconditions"),
    ]

    operations = [
        migrations.AddField(
            model_name="transaction",
            name="date",
            field=models.DateField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]