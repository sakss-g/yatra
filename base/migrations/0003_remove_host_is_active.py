# Generated by Django 4.1.5 on 2023-01-07 09:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0002_alter_host_address_alter_host_citizenship_id_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="host", name="is_active",),
    ]
