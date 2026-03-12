from django.urls import path
from . import views

urlpatterns = [
    path('categorys/', views.CategoryView.as_view()),
    path('category/<str:id>/', views.CategoryDetailView.as_view()),
    path('products/', views.ProductView.as_view()),
    path('product/<str:id>/', views.ProductDetailView.as_view()),
    path('addtocart/<str:id>/', views.AddToCartView.as_view()),
    path('mycart/', views.myCartView.as_view()),
    path('managecart/<str:id>/', views.ManageCartView.as_view()),
    path('checkout/', views.CheckoutView.as_view()),  # Fix: CheckoutView existed in views.py but was missing from urls
]