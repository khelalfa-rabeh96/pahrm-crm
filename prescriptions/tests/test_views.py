import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import datetime

from prescriptions.models import ChronicPrescription, PrescriptionItem
from prescriptions.serializers import ChronicPrescriptionSerializer, PrescriptionItemSerializer

class ChronicPrescriptionListViewTestCase(APITestCase):

    def setUp(self):
        self.url = reverse('chronic_prescription_list')

        presc = ChronicPrescription.objects.create()
        

    
    def test_get_returns_json_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
    
    def test_return_prescription_list(self):
        response = self.client.get(self.url)
        data = json.loads(response.content.decode('utf8'))
        serializer = ChronicPrescriptionSerializer(ChronicPrescription.objects.first())
        self.assertIn(serializer.data, data)
    
    
    def test_post_new_prescription_with_no_data(self):
        response = self.client.post(self.url)
        response_data = json.loads(response.content.decode('utf8'))


        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data['duration'], 90)
        self.assertTrue(response_data['notification_status'])
    
    def test_post_new_prescription_with_data(self):
        response = self.client.post( self.url,
         {
            "duration": 60, 
            "date": datetime.date.today() - datetime.timedelta(days=5)
        })
        response_data = json.loads(response.content.decode('utf8'))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data['duration'], 60)
        self.assertTrue(response_data['notification_status'])
    
    def test_for_invalid_duration_returns_error_code(self):
        response = self.client.post( self.url,
         {
            "duration": 150, 
        })
        response_data = json.loads(response.content.decode('utf8'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
class ChronicPrescrionDetailViewTestCase(APITestCase):

    def setUp(self):
        self.presc = ChronicPrescription.objects.create()
        self.url = reverse('chronic_prescription_detail', kwargs={'pk': self.presc.chronic_prescription_id})
        item_data = {'drug_name':"Dolipran cp 1g", 'quantity':1, 'prescription':self.presc}
        self.item = PrescriptionItem.objects.create(**item_data)


    def test_get_returns_json_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
    
    def test_retrieve_prescription_detail(self):
        response = self.client.get(self.url)
        prescr_serializer = ChronicPrescriptionSerializer(instance=self.presc)
        response_data = json.loads(response.content.decode('utf8'))
        self.assertEqual(response_data, prescr_serializer.data)
    
    def test_retrieve_prescription_related_item(self):
        # New prescription with its  new Item
        new_presc = ChronicPrescription.objects.create()
        data = {'drug_name':"Expandol cp 1g", 'quantity':11, 'prescription':new_presc}
        new_item = PrescriptionItem.objects.create(**data)
        new_item_serializer = PrescriptionItemSerializer(new_item)

        old_item_serializer =  PrescriptionItemSerializer(self.item)
        response = self.client.get(self.url)
        response_data = json.loads(response.content.decode('utf8'))
        prescr_serializer = ChronicPrescriptionSerializer(instance=self.presc)

        self.assertIn(old_item_serializer.data, prescr_serializer.data['drugs'])
        self.assertNotIn(new_item_serializer.data, prescr_serializer.data['drugs'])
    
    # Test adding new item to a prescription
    def test_posting_new_item_to_prescription(self):
        new_item_data = {
            'prescription': self.presc.chronic_prescription_id,
            'drug_name': 'Loratadine cp 10mg',
            'quantity': 15
            }
        
        prescr_serializer = ChronicPrescriptionSerializer(self.presc)
        self.assertEqual(len(prescr_serializer.data['drugs']), 1)
        
        response = self.client.post(self.url, new_item_data)
        response_data = json.loads(response.content.decode('utf-8'))

        prescr_serializer = ChronicPrescriptionSerializer(self.presc)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(prescr_serializer.data['drugs']), 2)
        
        new_item = PrescriptionItemSerializer(PrescriptionItem.objects.last())
        self.assertIn(new_item.data, prescr_serializer.data['drugs'])
        self.assertEqual(new_item.data['drug_name'], new_item_data['drug_name'])
        self.assertEqual(new_item.data['quantity'], new_item_data['quantity'])


    def test_edit_prescription(self):
        updated_data = {'chronic_prescription_id': self.presc.chronic_prescription_id, 'duration': 60}
        old_notification_status = self.presc.notification_status
        old_duration = self.presc.notification_status

        response = self.client.put(self.url, updated_data)
        response_data = json.loads(response.content.decode('utf8'))

        self.assertEqual(response.status_code,  status.HTTP_200_OK)
        self.assertEqual(response_data['notification_status'], old_notification_status)
        self.assertNotEqual(response_data['duration'], old_duration)
    
    def test_delete_prescription(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ChronicPrescription.objects.all().count(), 0)





    

    
        
