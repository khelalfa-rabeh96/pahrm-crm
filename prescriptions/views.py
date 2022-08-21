from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


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

class ChronicPrescriptionDetailView(APIView):
    serializer_class = ChronicPrescriptionSerializer

    def get(self, request, pk, format=None):
        presc = get_object_or_404(ChronicPrescription, pk=pk)
        serializer = self.serializer_class(presc)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        presc = get_object_or_404(ChronicPrescription, pk=pk)
        serializer = self.serializer_class(presc, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        presc = get_object_or_404(ChronicPrescription, pk=pk)
        presc.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

