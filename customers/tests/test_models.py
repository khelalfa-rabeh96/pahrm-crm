from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from customers.models import Customer

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

    def test_phone_number_replicated(self):
        Customer.objects.create(customer_name="John Doe", phones=["0795265877"])

        anna = Customer(customer_name="Anna", phones=["0795265877"])
        with self.assertRaises(ValidationError):
            anna.full_clean()
    
    def test_add_phone_number_(self):
        john = Customer.objects.create(customer_name="John Doe", phones=["0795265877"])

        self.assertEqual(len(john.phones), 1)
        john.add_phone_number('055568497721')
        self.assertEqual(len(john.phones), 2)
    
    def test_delete_phone_number(self):
        john = Customer.objects.create(customer_name="John Doe", phones=["0795265877", '055568497721'])

        self.assertEqual(len(john.phones), 2)
        john.delete_phone_number('055568497721')
        self.assertEqual(len(john.phones), 1)

    def test_customer_type_restriction(self):
        john = Customer(customer_name="John Doe", customer_type="player")

        with self.assertRaises(ValidationError):
            john.save()
            john.full_clean()
        
        

        


    
 
