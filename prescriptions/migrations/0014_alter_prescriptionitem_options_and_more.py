# Generated by Django 4.1 on 2022-08-22 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prescriptions', '0013_rename_chronic_presecription_id_chronicprescription_chronic_prescription_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='prescriptionitem',
            options={'managed': True},
        ),
        migrations.AlterField(
            model_name='prescriptionitem',
            name='drug_name',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterUniqueTogether(
            name='prescriptionitem',
            unique_together={('drug_name', 'prescription')},
        ),
    ]
