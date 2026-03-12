from django.db import models

import uuid
import secrets
from .paystack import Paystack

from users.models import Profile


class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)  # Fix: was DateTimeField (missing models.)

    def __str__(self):
        return self.title  # Fix: was self.name — Category has no 'name' field


#       PRODUCT MODEL
class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveBigIntegerField()
    discount_price = models.PositiveBigIntegerField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    main = models.ImageField(upload_to='products')
    photo1 = models.ImageField(upload_to='products', null=True, blank=True)
    photo2 = models.ImageField(upload_to='products', null=True, blank=True)
    photo3 = models.ImageField(upload_to='products', null=True, blank=True)
    photo4 = models.ImageField(upload_to='products', null=True, blank=True)
    product_id = models.UUIDField(default=uuid.uuid4, unique=True)
    is_available = models.BooleanField(default=True)
    in_stock = models.BigIntegerField()
    rating = models.BigIntegerField()
    reviews = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # Fix: was _str__ (missing leading underscore)
        return self.title

    def save(self, *args, **kwargs):
        if not self.product_id:
            self.product_id = uuid.uuid4()
        super().save(*args, **kwargs)


class Cart(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{str(self.total)}'


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart Product - {self.cart.id} - {self.quantity}'


#       ORDER MODEL
ORDER_STATUS = (
    ('Pending', 'Pending'),
    ('Cancel', 'Cancel'),
    ('Complete', 'Complete'),
)
PAYMENT_METHOD = (
    ('Paystack', 'Paystack'),
    ('Paypal', 'Paypal'),
    ('Bank Transfer', 'Bank Transfer'),
)


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    order_by = models.CharField(max_length=255)  # Fix: was models.ChartField (typo)
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS, default='Pending')
    shipping_address = models.TextField()
    mobile = models.CharField(max_length=50)
    email = models.EmailField()
    amount = models.PositiveBigIntegerField(default=0)
    subtotal = models.PositiveBigIntegerField(default=0)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD, default='Paystack')
    payment_complete = models.BooleanField(default=False)  # Fix: was missing but used in verify_payment()
    ref = models.CharField(max_length=255, null=True, blank=True)  # Fix: missing comma before null=True

    def __str__(self):
        return f'{self.amount} - {str(self.id)}'

    # auto save ref
    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = secrets.token_urlsafe(6)
        super().save(*args, **kwargs)

    # verifying payments on paystack
    def verify_payment(self):
        paystack = Paystack()  # Fix: was paystack = paystack() (name collision + wrong class case)
        status, result = paystack.verify_payment(self.ref, self.amount)  # Fix: was Paystack.verify_Payment (wrong case + uninstantiated)
        if status and result.get('status') == 'success':
            # ensure the amount matches
            if result['amount'] / 100 == self.amount:
                self.payment_complete = True
                self.save()
                return True
        return False