from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import ChronicPrescription
from .serializers import ChronicPrescriptionSerializer

class ChronicPrescriptionListView(APIView):
    serializer_class = ChronicPrescriptionSerializer

    def get(self, request, format=None):
        prescriptions = ChronicPrescription.objects.all()
        serializer  = self.serializer_class(prescriptions, many=True)

        return Response(serializer.data)
    
    def post(self, request, format=None):
     
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
