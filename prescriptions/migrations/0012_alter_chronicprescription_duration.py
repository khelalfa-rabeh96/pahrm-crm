# Generated by Django 4.1 on 2022-08-19 13:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prescriptions', '0011_alter_chronicprescription_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chronicprescription',
            name='duration',
            field=models.PositiveIntegerField(default=90, validators=[django.core.validators.MaxValueValidator(90), django.core.validators.MinValueValidator(30)]),
        ),
    ]