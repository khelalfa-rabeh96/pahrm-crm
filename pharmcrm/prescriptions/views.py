from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
import datetime
from django.db.models import  F


from .models import ChronicPrescription, PrescriptionItem
from .serializers import ChronicPrescriptionSerializer, PrescriptionItemSerializer

class ChronicPrescriptionListView(APIView, PageNumberPagination):
    serializer_class = ChronicPrescriptionSerializer

    def get_queryset(self):
        queryset = ChronicPrescription.objects.all()
        drug_name = self.request.query_params.get('drug_name')
        if drug_name is not None:
            queryset = queryset.filter(drugs__drug_name__icontains=drug_name).all()
        
        # comming soon is True only if: 0 < left days to serve the prescription again  < 15   
        # left_days = (today() - (date + duration))
        # comming soon is True only if: today - duration <= prescr_date <= today - duration - 15
        comming_soon = self.request.query_params.get('comming_soon')
        if comming_soon is not None or comming_soon == '' :
            queryset = queryset.filter(date__lte=datetime.date.today() - (
                datetime.timedelta(days=1)*F('duration') - 
                datetime.timedelta(days=15) 
                )).filter(date__gte=datetime.date.today() - (datetime.timedelta(days=1) * F('duration')))
        
        # Filter prescriptions that includ a given drug 
        medication = self.request.query_params.get('medication')
        if medication  :
            queryset = queryset.filter(drugs__drug_name__icontains=medication)
        
        # Filter prescriptions that concern a given customer
        customer = self.request.query_params.get('customer')
        if customer :
            queryset = queryset.filter(customer__customer_name__icontains=customer)
            
        return queryset

    def get(self, request, format=None):
        prescriptions = self.get_queryset()
        prescriptions_pg = self.paginate_queryset(prescriptions, request, view=self)
        serializer  = self.serializer_class(prescriptions_pg, many=True)
        return self.get_paginated_response(serializer.data)
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChronicPrescriptionDetailView(APIView):
    def get(self, request, pk, format=None):
        presc = get_object_or_404(ChronicPrescription, pk=pk)
        serializer = ChronicPrescriptionSerializer(presc)
        return Response(serializer.data)
    
    # Adding new item to this prescription
    def post(self, request, pk, format=None):
        presc = get_object_or_404(ChronicPrescription, pk=pk)
        item_data  = request.data.copy()
        item_data['prescription'] = presc.chronic_prescription_id
        serializer = PrescriptionItemSerializer(data=item_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk, format=None):
        presc = get_object_or_404(ChronicPrescription, pk=pk)
        serializer = ChronicPrescriptionSerializer(presc, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        presc = get_object_or_404(ChronicPrescription, pk=pk)
        presc.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PrescriptionItemDetailView(APIView):
    serializer_class = PrescriptionItemSerializer

    def get(self, request, pk, format=None):
        item = get_object_or_404(PrescriptionItem, pk=pk)
        serializer = self.serializer_class(item)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        item = get_object_or_404(PrescriptionItem, pk=pk)
        item_serializer = PrescriptionItemSerializer(item)

        data = request.data.copy()

        if data.get('drug_name') is None :
            data['drug_name'] = item_serializer.data['drug_name']
        
        if data.get('quantity') is None :
            data['quantity'] = item_serializer.data['quantity']
        
        if data.get('prescription') is None :
            data['prescription'] = item_serializer.data['prescription']

        serializer = self.serializer_class(item, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk, format=None):
        item = get_object_or_404(PrescriptionItem, pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
