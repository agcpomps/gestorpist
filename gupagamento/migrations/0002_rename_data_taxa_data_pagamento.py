# Generated by Django 4.2.7 on 2023-12-20 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("gupagamento", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="taxa", old_name="data", new_name="data_pagamento",
        ),
    ]
