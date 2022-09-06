from django.test import TestCase
from django.db import IntegrityError
import datetime


from prescriptions.serializers import PrescriptionItemSerializer, ChronicPrescriptionSerializer
from prescriptions.models import ChronicPrescription, PrescriptionItem
from customers.models import Customer


class PrescriptionItemTestCase(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(customer_name="John Doe")
        self.presc = ChronicPrescription.objects.create(customer=self.customer)
        self.item_data = {'drug_name': 'Amoxicilline EG cp 1g b/14',
                'quantity': 15,
                'prescription': self.presc}
        PrescriptionItem.objects.create(**self.item_data)
    
    def test_contains_expected_fields(self):
        expected_fields = ['prescription_item_id', 'drug_name', 'quantity', 'prescription']

        item = PrescriptionItem.objects.first()
        item_serializer = PrescriptionItemSerializer(item)

        self.assertEqual(set(item_serializer.data.keys()), set(expected_fields))

    def test_serializer_data_content(self):
        item = PrescriptionItem.objects.first()
        item_serializer = PrescriptionItemSerializer(item)

        self.assertEqual(item_serializer.data['drug_name'], self.item_data['drug_name'])
        self.assertEqual(item_serializer.data['quantity'],  self.item_data['quantity'])

    def test_item_serializer_related_to_prescription_serializer(self):
       
        item = PrescriptionItem.objects.first()

        prescription_serializer = ChronicPrescriptionSerializer(self.presc)
        item_serializer = PrescriptionItemSerializer(item)
        
        self.assertEqual(item_serializer.data['prescription'], self.presc.chronic_prescription_id)
        self.assertIn(item_serializer.data, prescription_serializer.data['drugs'])
    
        
    
    def test_quantity_lower_bound_constraint(self):
        item_data = {'drug_name': 'Dolipran cp 1g',
                'quantity': 15,
                'prescription': self.presc.chronic_prescription_id}

        item_data['quantity'] = -15
        item_serializer = PrescriptionItemSerializer(data=item_data)
        
        if item_serializer.is_valid():
            item_serializer.save()

        self.assertFalse(item_serializer.is_valid())
        self.assertEqual(set(item_serializer.errors), set(['quantity']))
    
    def test_unique_item_by_drug_name_with_the_same_prescription(self):
        data1 = {'drug_name': 'Dolipran cp 1g',
                'quantity': 15,
                'prescription': self.presc.chronic_prescription_id}

        serializer1 = PrescriptionItemSerializer(data=data1)
        if serializer1.is_valid():
            serializer1.save()
        self.assertTrue(serializer1.is_valid())

        # Replicated drug name in the same prescription 
        serializer2 = PrescriptionItemSerializer(data=data1)
        if serializer2.is_valid():
            serializer2.save()
        self.assertFalse(serializer2.is_valid())

        prescr2 = ChronicPrescription.objects.create(customer=self.customer)
        data1['prescription'] = prescr2.chronic_prescription_id

        serializer2 = PrescriptionItemSerializer(data=data1)
        if serializer2.is_valid():
            serializer2.save()
        self.assertTrue(serializer2.is_valid())



class ChronicPrescriptionTestCase(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(customer_name="John Doe")

    def test_contains_expected_fields(self):
        expected_fields = ['chronic_prescription_id', 'date', 'duration', 'notification_status', 'drugs', 'left_days', 'customer']
        
        prescr = ChronicPrescription.objects.create(customer=self.customer)
        prescr_serializer = ChronicPrescriptionSerializer(prescr)

        self.assertEqual(set(prescr_serializer.data.keys()), set(expected_fields))
    
    def test_default_duration(self):
        prescr = ChronicPrescription.objects.create(customer=self.customer)
        prescr_serializer = ChronicPrescriptionSerializer(prescr)
        self.assertEqual(prescr_serializer.data['duration'], 90)
    
    def test_upper_bound_duration(self):
        prescr_serializer = ChronicPrescriptionSerializer(data={'duration': 1000, 'customer': self.customer.id})
        
        if prescr_serializer.is_valid():
            prescr_serializer.save()
        self.assertFalse(prescr_serializer.is_valid())
        self.assertEqual(set(prescr_serializer.errors), set(['duration']))

    def test_lower_bound_duration(self):
        prescr_serializer = ChronicPrescriptionSerializer(data={'duration': 29,  'customer': self.customer.id})
        
        if prescr_serializer.is_valid():
            prescr_serializer.save()
        self.assertFalse(prescr_serializer.is_valid())
        self.assertEqual(set(prescr_serializer.errors), set(['duration']))

    def test_date_upper_bound(self):
        prescr_serializer = ChronicPrescriptionSerializer(data={'date': datetime.date.today() + datetime.timedelta(days=1),  'customer': self.customer.id})
        
        if prescr_serializer.is_valid():
            prescr_serializer.save()
        self.assertFalse(prescr_serializer.is_valid())
        self.assertEqual(set(prescr_serializer.errors), set(['date']))
    
    def test_date_lower_bound(self):
        prescr_serializer = ChronicPrescriptionSerializer(data={'date': datetime.date.today() - datetime.timedelta(days=91),  'customer': self.customer.id})
        
        if prescr_serializer.is_valid():
            prescr_serializer.save()
        self.assertFalse(prescr_serializer.is_valid())
        self.assertEqual(set(prescr_serializer.errors), set(['date']))
    
    def test_get_left_days(self):
        presc = ChronicPrescription.objects.create(**{
            'date': datetime.date.today() - datetime.timedelta(days=60),
            'duration': 45,
            'customer': self.customer
            })
        

        # Expected day to be served
        serving_day = presc.date + datetime.timedelta(days=presc.duration)
        today = datetime.date.today()
        delta = serving_day - today 

        # left days to be served
        expected_left_days = delta.days 

        serializer = ChronicPrescriptionSerializer(presc)
        self.assertEqual(expected_left_days, serializer.data['left_days'])


    
    
    

 
