from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

CUSTOMER_TYPE = (
    ('patient', 'Patient'),
    ('copharmacy', 'CoPharmacy')
)

def validate_phone_number(value):
    if value.isnumeric() == False:
        raise ValidationError(
            _('%(value)s contains non digits characters, only digits allowed'),
            params={'value': value},
        )



def prevent_replicated_phone(phone):
    phone_holders = Customer.objects.filter(phones__contains=[phone]).count()
    if phone_holders > 0 :
        raise ValidationError(
            _('%(value)s already holded by another customer'),
            params={'phone': phone},
        )




class Customer(models.Model):
    def __str__(self) :
        return self.customer_name

    id = models.BigAutoField(primary_key=True)
    customer_name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    phones = ArrayField(models.CharField(max_length=10, validators=[validate_phone_number, prevent_replicated_phone]), 
                                        default=list, null=True, blank=True)
    customer_type = models.CharField(max_length=10,default='patient', choices=CUSTOMER_TYPE)


    def add_phone_number(self, phone):
        self.phones.append(phone)
        self.save()
    
    def delete_phone_number(self, phone):
        self.phones.remove(phone)
        self.save()
