from rest_framework import fields, serializers
from .models import Courier, Order
from django.contrib.auth.models import User


class CourierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Courier
        fields = '__all__'
        lookup_field = 'courier_id'


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'
        lookup_field = 'order_id'

