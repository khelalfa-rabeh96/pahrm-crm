# Generated by Django 4.1 on 2022-08-25 13:21

import customers.models
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0006_alter_customer_phones'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phones',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=10, null=True, unique=True, validators=[customers.models.validate_phone_number]), default=list, size=None),
        ),
    ]