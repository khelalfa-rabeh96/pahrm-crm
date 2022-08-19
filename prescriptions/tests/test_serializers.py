from django.test import TestCase
from django.db import IntegrityError
import datetime

from prescriptions.serializers import PrescriptionItemSerializer, ChronicPrescriptionSerializer
from prescriptions.models import ChronicPrescription, PrescriptionItem

class PrescriptionItemTestCase(TestCase):
    def setUp(self):
        self.presc = ChronicPrescription.objects.create()
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
        
        self.assertEqual(item_serializer.data['prescription'], self.presc.chronic_presecription_id)
        self.assertIn(item_serializer.data, prescription_serializer.data['drugs'])
    
        
    
    def test_quantity_lower_bound_constraint(self):
        item_data = {'drug_name': 'Dolipran cp 1g',
                'quantity': 15,
                'prescription': self.presc.chronic_presecription_id}

        item_data['quantity'] = -15
        item_serializer = PrescriptionItemSerializer(data=item_data)
        
        if item_serializer.is_valid():
            item_serializer.save()

        self.assertFalse(item_serializer.is_valid())
        self.assertEqual(set(item_serializer.errors), set(['quantity']))
    
    def test_unique_item_by_name(self):
        data1 = {'drug_name': 'Dolipran cp 1g',
                'quantity': 15,
                'prescription': self.presc.chronic_presecription_id}

        serializer1 = PrescriptionItemSerializer(data=data1)
        if serializer1.is_valid():
            serializer1.save()
        self.assertTrue(serializer1.is_valid())

        # Replicated data 
        serializer2 = PrescriptionItemSerializer(data=data1)
        if serializer2.is_valid():
            serializer2.save()
        self.assertFalse(serializer2.is_valid())


class ChronicPrescriptionTestCase(TestCase):
    def test_contains_expected_fields(self):
        expected_fields = ['chronic_presecription_id', 'date', 'duration', 'notification_status', 'drugs']
        
        prescr = ChronicPrescription.objects.create()
        prescr_serializer = ChronicPrescriptionSerializer(prescr)

        self.assertEqual(set(prescr_serializer.data.keys()), set(expected_fields))
    
    def test_default_duration(self):
        prescr = ChronicPrescription.objects.create()
        prescr_serializer = ChronicPrescriptionSerializer(prescr)
        self.assertEqual(prescr_serializer.data['duration'], 90)
    
    def test_upper_bound_duration(self):
        prescr_serializer = ChronicPrescriptionSerializer(data={'duration': 1000})
        
        if prescr_serializer.is_valid():
            prescr_serializer.save()
        self.assertFalse(prescr_serializer.is_valid())
        self.assertEqual(set(prescr_serializer.errors), set(['duration']))

    def test_lower_bound_duration(self):
        prescr_serializer = ChronicPrescriptionSerializer(data={'duration': 29})
        
        if prescr_serializer.is_valid():
            prescr_serializer.save()
        self.assertFalse(prescr_serializer.is_valid())
        self.assertEqual(set(prescr_serializer.errors), set(['duration']))

    def test_date_upper_bound(self):
        prescr_serializer = ChronicPrescriptionSerializer(data={'date': datetime.date.today() + datetime.timedelta(days=1)})
        
        if prescr_serializer.is_valid():
            prescr_serializer.save()
        self.assertFalse(prescr_serializer.is_valid())
        self.assertEqual(set(prescr_serializer.errors), set(['date']))
    
    def test_date_lower_bound(self):
        prescr_serializer = ChronicPrescriptionSerializer(data={'date': datetime.date.today() - datetime.timedelta(days=91)})
        
        if prescr_serializer.is_valid():
            prescr_serializer.save()
        self.assertFalse(prescr_serializer.is_valid())
        self.assertEqual(set(prescr_serializer.errors), set(['date']))
    

 
