from rest_framework import serializers
from .models import *


# :: CATEGORY SERIALIZER
class CategorySerializer(serializers.ModelSerializer):  # Fix: was serializer.Modelserializer (wrong module + wrong case)
    class Meta:
        model = Category
        fields = '__all__'  # Fix: was '_all_' (wrong string)


# :: PRODUCT SERIALIZER
class ProductSerializer(serializers.ModelSerializer):  # Fix: was Modelserializer (wrong case)
    class Meta:
        model = Product
        fields = '__all__'  # Fix: was '_all_'


# :: CART SERIALIZER
class CartSerializer(serializers.ModelSerializer):  # Fix: was Modelserializer (wrong case)
    class Meta:
        model = Cart
        fields = '__all__'  # Fix: was '_all_'


# :: CART PRODUCT SERIALIZER
class CartProductSerializer(serializers.ModelSerializer):  # Fix: was Modelserializer (wrong case)
    class Meta:
        model = CartProduct
        fields = '__all__'  # Fix: was '_all_'


# :: ORDER SERIALIZER
class OrderSerializer(serializers.ModelSerializer):  # Fix: was Modelserializer (wrong case)
    class Meta:
        model = Order
        fields = '__all__'  # Fix: was '_all_'


# :: CHECKOUT SERIALIZER
class CheckoutSerializer(serializers.ModelSerializer):  # Fix: was Modelserializer (wrong case)
    class Meta:
        model = Order
        exclude = ['cart', 'amount', 'order_status', 'subtotal', 'payment_complete', 'ref']