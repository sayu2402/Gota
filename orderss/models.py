from django.db import models

# Create your models here.
from django.db import models
from account.models import Account
from products.models import Product , Variation
from django.core.validators import MinLengthValidator, MaxLengthValidator
from categories.models import Category

# Create your models here.

class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id



class Order(models.Model):

    STATUS = {
        ('New' , 'New'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Shipped' , 'Shipped')
    }

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    order_product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=250)
    address = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    pincode = models.IntegerField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    order_note = models.TextField(max_length=200)
    order_total = models.FloatField()
    tax = models.FloatField()
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=100, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=50)
    is_orderd = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    orderd = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name
