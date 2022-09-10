import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from customers.models import Customer
from customers.serializers import CustomerSerializer


class CustomerListViweTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('customer_list')
        
    
    def test_get_returns_json_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
    
    
    def test_retrieve_customer_list(self):
        john = Customer.objects.create(customer_name="John Doe")
        larry = Customer.objects.create(customer_name="Larry")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf8'))
        customer_list = response_data.get('results', [])

        john_serializer = CustomerSerializer(john)
        larry_serializer = CustomerSerializer(larry)
        self.assertIn(john_serializer.data, customer_list)
        self.assertIn(larry_serializer.data, customer_list)
        self.assertEqual(len(customer_list), 2)
    
    def test_post_new_customer(self):
        new_customer = {"customer_name": "Erik"}
        response = self.client.post(self.url, data=new_customer)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = json.loads(response.content.decode('utf8'))
        self.assertEqual(response_data.get('customer_name'), new_customer.get('customer_name'))
        self.assertEqual(Customer.objects.all().count(), 1)
    
    def test_post_new_customer_with_invalid_customer_type(self):

        new_customer = {"customer_name": "Erik", "customer_type": "teacher"}
        response = self.client.post(self.url, data=new_customer)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Customer.objects.all().count(), 0)
    
    def test_post_new_customer_with_invalid_phone_number(self):
        new_customer = {"customer_name": "Erik", "phones": ["079526sd"]}
        response = self.client.post(self.url, data=new_customer)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Customer.objects.all().count(), 0)

class CustomerDetailViewTestCase(APITestCase):
    def setUp(self):
        customer = Customer.objects.create(customer_name="Mark")
        self.url = reverse('customer_detail', kwargs={'pk': customer.id})

    
    def test_get_returns_json_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
    
    def test_get_customer_detail(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mark = Customer.objects.first()

        response_data = json.loads(response.content.decode('utf8'))
        self.assertEqual(response_data, CustomerSerializer(mark).data)
    

    def test_update_cutomer(self):
        mark = Customer.objects.first()
        updated_data = {"id" : mark.id, "customer_name": mark.customer_name ,"customer_type": "copharmacy"}
        
        response = self.client.put(self.url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = json.loads(response.content.decode('utf8'))
        self.assertEqual(response_data.get('customer_type'), updated_data.get("customer_type"))

        mark = Customer.objects.first()
        self.assertEqual(mark.customer_type, updated_data.get("customer_type"))
    

    def test_partial_update_cutomer(self):
        mark = Customer.objects.first()
        self.assertEqual(len(mark.phones), 0)

        updated_data = {"phones": ["0795265877"]}
        response = self.client.patch(self.url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response_data = json.loads(response.content.decode('utf8'))
        mark = Customer.objects.first()
        self.assertEqual(response_data.get('phones'), updated_data.get("phones"))
        self.assertEqual(len(mark.phones), 1)
        self.assertIn("0795265877" ,mark.phones)
    
    def test_delete_customer(self):
        mark = Customer.objects.first()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        customer_count = Customer.objects.all().count()
        self.assertEqual(customer_count, 0)



    



    