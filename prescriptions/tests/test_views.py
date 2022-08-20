import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import datetime

from prescriptions.models import ChronicPrescription, PrescriptionItem
from prescriptions.serializers import ChronicPrescriptionSerializer

class ChronicPrescriptionListViewTestCase(APITestCase):

    def setUp(self):
        self.url = reverse('chronic_prescription_list')

        presc = ChronicPrescription.objects.create()
        

    
    def test_get_returns_json_200(self):
        response = self.client.get(self.url)
        self.assertTrue(response.status_code, status.HTTP_200_OK)
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
    




