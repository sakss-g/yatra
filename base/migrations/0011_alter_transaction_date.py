# Generated by Django 4.1.5 on 2023-03-30 04:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0010_alter_transaction_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="date",
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
