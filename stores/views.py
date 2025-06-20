from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status,serializers

from . serializers import *
from . models import *

#    CATEGORY
class CategoryView(APIView):
    def get(self,request):
        try:
            category = Category.objects.all()
            serializer = CategorySerializer(categories,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# Compare this snippet from stores/serializers.py:

    def post(self,request):
        try:
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# Compare this snippet from stores/views.py:
class CategoryDetailView(APIView):
    def get(self,request,id):
        try:
            category = Category.objects.get(id=id)
            serializer = CategorySerializer(category)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self,request,id):
        try:
            category = get_object_or_404(Category,id=id)
            serializer = CategorySerializer(category,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self,request,id):
        try:
            category = get_object_or_404(Category,id=id)
            category.delete()
            return Response({"Message":f"{category.title} deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#    PRODUCT
class ProductView(APIView):
    def get(self,request):
        try:
            product = Product.objects.all()
            serializer = ProductSerializer(Product,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# Compare this snippet from stores/serializers.py:

    def post(self,request):
        try:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# Compare this snippet from stores/views.py:
class ProductDetailView(APIView):
    def get(self,request,id):
        try:
            product = Product.objects.get(id=id)
            serializer = ProductSerializer(Product)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self,request,id):
        try:
            product = get_object_or_404(Product,id=id)
            serializer = ProductSerializer(Product,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self,request,id):
        try:
            product = get_object_or_404(Product,id=id)
            product.delete()
            return Response({"Message":f"{category.title} deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
                return Response ({'error':str(e)},status=status)
        
class AddToCartView(APIView):
    def post(self,request,id):
        try:
            #get the product to add
            Product = get_object_or_404(Product, id=id)
            #Cart id 
            Cart_id = request.session.get('cart_id', None)

            while transaction.atomic():
                if Cart_id: 
                    cart = Cart.objects.filter(id)