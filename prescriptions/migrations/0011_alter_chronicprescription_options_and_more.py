# Generated by Django 4.1 on 2022-08-19 11:05

import datetime
from django.db import migrations, models
import prescriptions.models


class Migration(migrations.Migration):

    dependencies = [
        ('prescriptions', '0010_remove_chronicprescription_check_prescription_date_range_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chronicprescription',
            options={},
        ),
        migrations.RemoveConstraint(
            model_name='chronicprescription',
            name='check_prescription_date_range',
        ),
        migrations.AlterField(
            model_name='chronicprescription',
            name='date',
            field=models.DateField(default=datetime.date.today, validators=[prescriptions.models.no_future_date, prescriptions.models.no_old_date]),
        ),
    ]