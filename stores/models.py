from django.db import models

import uuid
import secrets
from . Paystack import paystack

from users.models import Profile

class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category',null=True,blank=True)
    created = DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
#       PRODUCT MODEL
class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveBigIntegerField()
    discount_price = models.PositiveBigIntegerField(null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    main = models.ImageField(upload_to='products')
    photo1 = models.ImageField(upload_to='products',null=True,blank=True)
    photo2 = models.ImageField(upload_to='products',null=True,blank=True)
    photo3 = models.ImageField(upload_to='products',null=True,blank=True)
    photo4 = models.ImageField(upload_to='products',null=True,blank=True)
    product_id = models.UUIDField(default=uuid.uuid4,unique=True)
    is_available = models.BooleanField(default=True)
    in_stock = models.BigIntegerField()
    rating = models.BigIntegerField()
    reviews = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def _str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        if  not self.product_id:
            self.product_id = uuid.uuid4()
        super().save(*args,**kwargs)

class Cart(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE, null=True,blank=True)
    total = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{str(self.total)}'
    
class CartProduct(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Cart Product - {self.cart.id} - {self.quantity}'
    
#       ORDER MODEL
ORDER_STATUS = (
    ('Pending','Pending'),
    ('Cancel','Cancel'),
    ('Complete','Complete'),
)
PAYMENT_METHOD = (
    ('Paystack','Paystack'),
    ('Paypal','Paypal'),
    ('Bank Transfer','Bank Transfer'),
)

class Order(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    order_by = models.ChartField(max_length=255)
    order_status = models.CharField(max_length=50,choices=ORDER_STATUS,default='Pending')
    shipping_address = models.TextField()
    mobile = models.CharField(max_length=50)
    email = models.EmailField()
    amount = models.PositiveBigIntegerField()
    subtotal = models.PositiveBigIntegerField()
    payment_method = models.CharField(max_length=50,choices=PAYMENT_METHOD,default='Paystack')
    ref = models.CharField(max_length=255 null=True,blank=True)

    def __str__(self):
        return f'{self.amount} - {str(self.id)}'
    
    # auto save ref
    def save(self,*args,**kwargs):
        if not self.ref:
            self.ref = secrets.token_urlsafe(6)
        super().save(*args,**kwargs)

    def __str__(self):
        return f'{self.amount} - {str(self.id)}'

    # vefifyingpayments on paystacks
    def verify_payment(self):
        paystack = paystack()
        status,result = Paystack.verify_Payment(self.ref,self.amount)
        if status and result.get('status') == 'success':
            # ensure the amount matches
            if result['amount']/100 ==self.amount:
                self.payment_complete = True
                # del self.cart
                self.save()
                return True
        # if payment is not successful
        return False