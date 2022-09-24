from django.test import TestCase
from django.db import IntegrityError

from customers.models import Customer
from customers.serializers import CustomerSerializer

class CustomerSerialzerTestCase(TestCase):

    def test_contain_expected_fields(self):
        expected_fields = ['id', 'customer_name', 'customer_type', 'phones']

        john = Customer.objects.create(customer_name="John Doe")
        john_serializer = CustomerSerializer(john)

        self.assertEqual(set(john_serializer.data.keys()), set(expected_fields))
    
    def test_phone_number_validation(self):
        new_customer = {"customer_name": "John Doe", "customer_type": "patient", "phones": ["0795265877", "0754q9745"]}
        new_customer_serializer = CustomerSerializer(data=new_customer)
        if (new_customer_serializer.is_valid()):
            new_customer_serializer.save()
        
        self.assertFalse(new_customer_serializer.is_valid())
        self.assertEqual(set(new_customer_serializer.errors), set(['phones']))
    
