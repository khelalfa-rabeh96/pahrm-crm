from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from customers.models import Customer
from prescriptions.models import ChronicPrescription

class CustomerModelTestCase(TestCase):
    
    def test_unique_name_constraint(self):
        Customer.objects.create(customer_name="John Doe", phones=["0795265877"])
        c2 = Customer(customer_name="John Doe")

        with  self.assertRaises(ValidationError):
            c2.full_clean()
    
    def test_optional_phone_number(self):
        Customer.objects.create(customer_name="John Doe")
        john = Customer.objects.first()

        self.assertEqual(Customer.objects.all().count(), 1)
        self.assertEqual(john.customer_name, "John Doe" )
        self.assertEqual(len(john.phones), 0)
    
    def test_phone_number_validation(self):
        Customer.objects.create(customer_name="John Doe", phones=["0795265877"])
        self.assertEqual(Customer.objects.all().count(), 1)

        anna = Customer(customer_name="Anna", phones=["055548697s"])
        with self.assertRaises(ValidationError):
            anna.full_clean()
        
        self.assertEqual(Customer.objects.all().count(), 1)
    

    def test_customer_type_restriction(self):
        john = Customer(customer_name="John Doe", customer_type="player")

        with self.assertRaises(ValidationError):
            john.save()
            john.full_clean()
    
    def test_customer_related_chronic_prescriptions(self):
        john = Customer.objects.create(customer_name="John Doe")
        presc1 = ChronicPrescription.objects.create(customer=john)

        mike = Customer.objects.create(customer_name="Mike Doe")
        presc2 = ChronicPrescription.objects.create(customer=mike)

        self.assertIn(presc1,john.chronic_prescription.all())
        self.assertNotIn(presc2,john.chronic_prescription.all())

        self.assertIn(presc2,mike.chronic_prescription.all())
        self.assertNotIn(presc1,mike.chronic_prescription.all())
    
    

        
        

        


    
 
