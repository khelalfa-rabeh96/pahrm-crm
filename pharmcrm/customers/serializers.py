from rest_framework import serializers
from .models import Customer
from django.core.exceptions import ValidationError


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields  = ('id', 'customer_name', 'customer_type', 'phones')