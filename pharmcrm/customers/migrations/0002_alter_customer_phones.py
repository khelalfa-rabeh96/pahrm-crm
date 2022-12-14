# Generated by Django 4.1 on 2022-09-21 09:27

import customers.models
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phones',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=10, validators=[customers.models.validate_phone_number]), blank=True, default=list, null=True, size=None),
        ),
    ]
