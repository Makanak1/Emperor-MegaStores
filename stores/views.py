from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.db import transaction
from rest_framework.response import Response  # Fix: removed invalid Session import
from rest_framework import status

from .serializers import *
from .models import *


#    CATEGORY
class CategoryView(APIView):
    def get(self, request):
        try:
            category = Category.objects.all()
            serializer = CategorySerializer(category, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryDetailView(APIView):
    def get(self, request, id):
        try:
            category = get_object_or_404(Category, id=id)
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        try:
            category = get_object_or_404(Category, id=id)
            serializer = CategorySerializer(category, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            category = get_object_or_404(Category, id=id)
            category.delete()
            return Response({"Message": f"{category.title} deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#    PRODUCT
class ProductView(APIView):
    def get(self, request):
        try:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)  # Fix: was passing class Product instead of queryset
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductDetailView(APIView):
    def get(self, request, id):
        try:
            product = get_object_or_404(Product, id=id)
            serializer = ProductSerializer(product)  # Fix: was passing class Product instead of instance
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        try:
            product = get_object_or_404(Product, id=id)
            serializer = ProductSerializer(product, data=request.data, partial=True)  # Fix: was passing class Product
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            product = get_object_or_404(Product, id=id)
            product.delete()
            return Response({"Message": f"{product.title} deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#    ADD TO CART
class AddToCartView(APIView):
    def post(self, request, id):
        try:
            product = get_object_or_404(Product, id=id)  # Fix: was Product = ... (shadowing the model class)
            cart_id = request.session.get('cart_id', None)

            with transaction.atomic():  # Fix: was 'while' (infinite loop) — should be 'with'
                if cart_id:
                    cart = Cart.objects.filter(id=cart_id).first()
                    if cart:  # Fix: inverted logic — original created new cart when cart WAS found
                        # Check if product is already in the cart
                        product_in_cart = cart.cartproduct_set.filter(product=product)
                        if product_in_cart.exists():
                            cart_product = product_in_cart.last()
                            cart_product.quantity += 1
                            cart_product.subtotal += product.price
                            cart_product.save()
                            cart.total += product.price
                            cart.save()
                            return Response({"Message": "Item quantity increased in cart"}, status=status.HTTP_200_OK)
                        else:
                            CartProduct.objects.create(cart=cart, product=product, quantity=1, subtotal=product.price)
                            cart.total += product.price
                            cart.save()
                            return Response({"Message": "Item added to cart"}, status=status.HTTP_201_CREATED)
                    else:
                        # Cart ID in session no longer valid — create a new cart
                        cart = Cart.objects.create(total=0)
                        request.session['cart_id'] = cart.id
                        CartProduct.objects.create(cart=cart, product=product, quantity=1, subtotal=product.price)
                        cart.total += product.price
                        cart.save()
                        return Response({"Message": "New cart created and item added"}, status=status.HTTP_201_CREATED)
                else:
                    # No cart session yet — create a fresh cart
                    cart = Cart.objects.create(total=0)
                    request.session['cart_id'] = cart.id
                    CartProduct.objects.create(cart=cart, product=product, quantity=1, subtotal=product.price)
                    cart.total += product.price
                    cart.save()
                    return Response({"Message": "New cart created and item added"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# My Cart
class myCartView(APIView):
    def get(self, request):
        try:
            cart_id = request.session.get('cart_id', None)
            if cart_id:
                cart = get_object_or_404(Cart, id=cart_id)
                serializer = CartSerializer(cart)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"Message": "No items in the cart"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Manage user Cart
class ManageCartView(APIView):
    def post(self, request, id):
        try:
            cart_id = request.session.get('cart_id', None)
            if cart_id:
                cart = get_object_or_404(Cart, id=cart_id)
                cart_product = get_object_or_404(CartProduct, id=id, cart=cart)
                action = request.data.get('action')

                if action == 'increase':
                    cart_product.quantity += 1
                    cart_product.subtotal += cart_product.product.price
                    cart_product.save()
                    cart.total += cart_product.product.price
                    cart.save()
                    return Response({"Message": "Item quantity increased"}, status=status.HTTP_200_OK)

                elif action == 'decrease':
                    if cart_product.quantity > 1:
                        cart_product.quantity -= 1
                        cart_product.subtotal -= cart_product.product.price
                        cart_product.save()
                        cart.total -= cart_product.product.price
                        cart.save()
                        return Response({"Message": "Item quantity decreased"}, status=status.HTTP_200_OK)
                    else:
                        # Fix: original checked quantity == 0 AFTER decrementing from 1, which is unreachable
                        # Instead, remove the item when quantity would reach 0
                        cart.total -= cart_product.subtotal
                        cart.save()
                        cart_product.delete()
                        return Response({"Message": "Item removed from cart"}, status=status.HTTP_200_OK)

                elif action == 'remove':
                    cart.total -= cart_product.subtotal
                    cart.save()
                    cart_product.delete()
                    return Response({"Message": "Item removed from cart"}, status=status.HTTP_200_OK)

                else:
                    return Response({"Message": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"Message": "No cart found"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Checkout user cart
class CheckoutView(APIView):
    def post(self, request):
        try:
            cart_id = request.session.get('cart_id', None)
            if cart_id:
                cart = get_object_or_404(Cart, id=cart_id)
                serializer = CheckoutSerializer(data=request.data)
                if serializer.is_valid():
                    order = serializer.save(cart=cart, subtotal=cart.total, amount=cart.total, order_status='Pending')
                    cart.delete()
                    request.session['cart_id'] = None
                    return Response({"Message": "Checkout successful", "order_id": order.id, "ref": order.ref}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"Message": "No items in the cart"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)