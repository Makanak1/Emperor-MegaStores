from rest_framework import serializers
from . models import *

# :: CATEGORY SERIALIZER
class CategorySerializer(serializer.Modelserializer):
    class Meta:
        model=Category
        fields='_all_'

# :: PRODUCT SERIALIZER
class ProductSerializer(serializers.Modelserializer):
    class Meta:
        model=Product
        fields='_all_'

# :: CART SERIALIZER
class CartSerializer(serializers.Modelserializer):
    class Meta:
        model=Cart
        fields='_all_'

# :: CART  PRODUCT SERIALIZER
class CartProductSerializer(serializers.Modelserializer):
    class Meta:
        model=CartProduct
        fields='_all_'

# :: ORDER SERIALIZER
class OrderSerializer(serializers.Modelserializer):
    class Meta:
        model=Order
        fields='_all_'

# :: CHECKOUT SERIALIZER
class CheckoutSerializer(serializers.Modelserializer):
    class Meta:
        model=Order
        exclude=['cart','amount','order_status','subtotal','payment_complete','ref']