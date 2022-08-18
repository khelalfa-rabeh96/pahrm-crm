# Generated by Django 4.1 on 2022-08-18 13:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prescriptions', '0003_remove_chronicprescription_check_no_future_prescription_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='chronicprescription',
            name='check_no_future_prescription',
        ),
        migrations.AddConstraint(
            model_name='chronicprescription',
            constraint=models.CheckConstraint(check=models.Q(('date__lte', datetime.datetime(2022, 8, 18, 13, 25, 33, 369396, tzinfo=datetime.timezone.utc))), name='check_no_future_prescription'),
        ),
    ]
