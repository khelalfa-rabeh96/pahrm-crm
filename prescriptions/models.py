from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models import CheckConstraint, Q, F
import datetime



def no_future_date(value):
    today = datetime.date.today()
    if value > today:
        raise ValidationError('Prescription_Date cannot be in the future.')

def no_old_date(value):
    today = datetime.date.today()
    if value < (today - datetime.timedelta(days = 90)):
        raise ValidationError('Prescription_Date cannot be too old.')

# Create your models here.
class ChronicPrescription(models.Model):
    chronic_prescription_id = models.AutoField(primary_key=True)
    date = models.DateField(default=datetime.date.today, validators=[no_future_date, no_old_date])
    # This field is for the prescription duration in days
    duration = models.PositiveIntegerField(default=90, validators=[MaxValueValidator(90), MinValueValidator(30)])
    notification_status = models.BooleanField(default=True)

    
   


class PrescriptionItem(models.Model):
    prescription_item_id = models.AutoField(primary_key=True)
    drug_name = models.CharField(max_length=250, null=False, blank=False, unique=True)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    prescription = models.ForeignKey('ChronicPrescription', on_delete=models.CASCADE, related_name="drugs")

