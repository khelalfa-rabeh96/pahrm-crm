from time import time
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.db.models import CheckConstraint, Q, F
import datetime


# Create your models here.
class ChronicPrescription(models.Model):
    chronic_presecription_id = models.AutoField(primary_key=True)
    date = models.DateField(default=datetime.date.today)
    # This field is for the prescription duration in days
    duration = models.PositiveIntegerField(default=90, validators=[MaxValueValidator(90)])
    notification_status = models.BooleanField(default=True)

    
   
    class Meta:
        managed = True 
        constraints = [
            # Check for the date range, it should be between 90 days ago and today.
            CheckConstraint(
                check = Q(date__lte=datetime.date.today()) & 
                Q(date__gte=datetime.date.today() - datetime.timedelta(days = 90)),
                name="check_prescription_date_range"
            ),
                     
        ]

class PrescriptionItem(models.Model):
    prescription_item_id = models.AutoField(primary_key=True)
    drug_name = models.CharField(max_length=250, null=False, blank=False, unique=True)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    prescription = models.ForeignKey('ChronicPrescription', on_delete=models.CASCADE, related_name="drugs")