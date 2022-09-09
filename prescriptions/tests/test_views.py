import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import datetime



from prescriptions.models import ChronicPrescription, PrescriptionItem
from prescriptions.serializers import ChronicPrescriptionSerializer, PrescriptionItemSerializer
from customers.models import Customer


class ChronicPrescriptionListViewTestCase(APITestCase):

    def setUp(self):
        self.url = reverse('chronic_prescription_list')
        self.customer = Customer.objects.create(customer_name="John Doe")
        self.presc = ChronicPrescription.objects.create(customer=self.customer)
        

    
    def test_get_returns_json_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
    
    def test_return_pagintation_prescription_list(self):
        response = self.client.get(self.url)
        data = json.loads(response.content.decode('utf8'))
        serializer = ChronicPrescriptionSerializer(ChronicPrescription.objects.first())
        self.assertIn(serializer.data, data['results'])
        self.assertEqual(data['count'], 1)
        self.assertIsNone(data['previous'])
        self.assertIsNone(data['next'])
    
    def test_search_prescritions_that_includ_a_given_drug(self):
        PrescriptionItem.objects.create(**{"drug_name": "Amoxicilline 1g", "quantity": 9, "prescription": self.presc})

        presc2 = ChronicPrescription.objects.create(customer=self.customer)
        PrescriptionItem.objects.create(**{"drug_name": "Clamoxyl 1g", "quantity": 4, "prescription": presc2})

        # prescription 1 contains 'amoxicilline' in its items while prescr2 does not
        response = self.client.get(self.url, {'drug_name': 'amoxicilline'})
        response_data = json.loads(response.content.decode('utf-8'))
        results = response_data['results']
        
        self.assertTrue(self.presc.chronic_prescription_id in [presc['chronic_prescription_id'] for presc in results])
        self.assertFalse(presc2.chronic_prescription_id in [presc['chronic_prescription_id'] for presc in results])
    
    # Fetch only prescriptions that will be serve again soon
    # prescription that has left less than 15 days should be notified
    # So the pharmacist can take in consediration to avoid missing any medication 
    # This prescription would has
    def test_get_only_comming_soon_prescriptions(self):
        p1 = ChronicPrescription.objects.create(
            date=datetime.date.today() - datetime.timedelta(days=70), # duration is 90 days, so there is 20 days left
            customer=self.customer
            ) 
        p2 = ChronicPrescription.objects.create(
            date=datetime.date.today() - datetime.timedelta(days=80), # duration is 90 days, so there is 10 days left
            customer=self.customer
            ) 
        p3 = ChronicPrescription.objects.create(
            date=datetime.date.today() - datetime.timedelta(days=50), # duration is 60 days, so there is 10 days left
            duration=60,
            customer=self.customer
            ) 

        response = self.client.get(self.url, {"comming_soon":""})
        response_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ids = [p['chronic_prescription_id'] for p in response_data['results']]

        self.assertNotIn(self.presc.chronic_prescription_id, ids)
        self.assertNotIn(p1.chronic_prescription_id, ids)
        self.assertIn(p2.chronic_prescription_id, ids)
        self.assertIn(p3.chronic_prescription_id, ids)



    
    def test_post_new_prescription_with_no_default_data(self):
        response = self.client.post(self.url, {'customer': self.customer.id})
        response_data = json.loads(response.content.decode('utf8'))


        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data['duration'], 90)
        self.assertTrue(response_data['notification_status'])
          
    
    
    def test_post_new_prescription_with_data(self):
        response = self.client.post( self.url,
         {
            "duration": 60, 
            "date": datetime.date.today() - datetime.timedelta(days=5),
            'customer': self.customer.id
            
        })
        response_data = json.loads(response.content.decode('utf8'))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data['duration'], 60)
        self.assertTrue(response_data['notification_status'])
    
    
    def test_for_invalid_duration_returns_error_code(self):
        response = self.client.post( self.url,
         {
            "duration": 150, 
            'customer': self.customer.id
        })
        response_data = json.loads(response.content.decode('utf8'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
class ChronicPrescrionDetailViewTestCase(APITestCase):

    def setUp(self):
        self.customer = Customer.objects.create(customer_name="John Doe")
        self.presc = ChronicPrescription.objects.create(customer=self.customer)
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
        new_presc = ChronicPrescription.objects.create(customer=self.customer)
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
            'quantity': 15,
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
        updated_data = {'chronic_prescription_id': self.presc.chronic_prescription_id, 
                        'duration': 60, 'customer': self.customer.id
                        }
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


class ChronicPrescriptionItemDetailTestCase(APITestCase):

    def setUp(self):
        self.customer =  Customer.objects.create(customer_name="John Doe")
        self.presc = ChronicPrescription.objects.create(customer=self.customer)
        self.item_data = {'drug_name':"Dolipran cp 1g", 'quantity':1, 'prescription':self.presc}
        self.item = PrescriptionItem.objects.create(**self.item_data)

        self.url = reverse('chronic_prescription_item_detail', kwargs={'pk': self.item.prescription_item_id})

    def test_get_returns_json_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
    
    def test_retrieve_prescription_item_detail(self):
        response = self.client.get(self.url)
        item_serializer = PrescriptionItemSerializer(instance=self.item)
        response_data = json.loads(response.content.decode('utf8'))
        self.assertEqual(response_data, item_serializer.data)
    
    def test_update_prescription_item(self):
        item_serializer = PrescriptionItemSerializer(self.item)
        data = {'drug_name':'new name', 'quantity': 10, 'prescription': item_serializer.data['prescription']}

        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        item = PrescriptionItem.objects.first()
        self.assertEqual(item.drug_name, data['drug_name'])
        self.assertEqual(item.quantity, data['quantity'])
    
    def test_partial_update_prscription_item(self):
        data = {"quantity": 20}
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        item = PrescriptionItem.objects.first()
        self.assertEqual(item.drug_name, self.item_data['drug_name'])
        self.assertNotEqual(item.quantity, self.item_data['quantity'])
        self.assertEqual(item.quantity, data['quantity'])
    

    def test_delete_prescription_item(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PrescriptionItem.objects.all().count(), 0)
        prescr_serializer = ChronicPrescriptionSerializer(self.presc)
        self.assertEqual(len(prescr_serializer.data.get('drugs')), 0)


    