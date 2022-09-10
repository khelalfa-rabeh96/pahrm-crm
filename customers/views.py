from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Customer 
from .serializers import CustomerSerializer

class CustomerModelViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = PageNumberPagination

    

