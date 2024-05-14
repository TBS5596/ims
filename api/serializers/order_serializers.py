from rest_framework import serializers

from order.models import Order, OrderItems

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = '__all__'