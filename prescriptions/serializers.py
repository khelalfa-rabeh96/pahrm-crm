from rest_framework import serializers
from .models import ChronicPrescription, PrescriptionItem

class PrescriptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionItem
        fields = ('prescription_item_id', 'drug_name', 'quantity', 'prescription')

class ChronicPrescriptionSerializer(serializers.ModelSerializer):
    drugs = PrescriptionItemSerializer(many=True, read_only=True)
    notification_status = serializers.BooleanField(default=True) 

    customer_name  = serializers.CharField(source='customer.customer_name', read_only=True)

    left_days = serializers.SerializerMethodField()
    def get_left_days(self, obj):
        return obj.count_left_days()

    class Meta:
        model = ChronicPrescription
        fields = ('chronic_prescription_id', 'date', 'duration', 'notification_status', 'left_days', 'drugs', 'customer', 'customer_name')