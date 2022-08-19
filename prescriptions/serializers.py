from rest_framework import serializers
from .models import ChronicPrescription, PrescriptionItem

class PrescriptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionItem
        fields = ('prescription_item_id', 'drug_name', 'quantity', 'prescription')

class ChronicPrescriptionSerializer(serializers.ModelSerializer):
    drugs = PrescriptionItemSerializer(many=True, read_only=True)
    class Meta:
        model = ChronicPrescription
        fields = ('chronic_presecription_id', 'date', 'duration', 'notification_status', 'drugs')