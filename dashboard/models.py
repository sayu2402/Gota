from django.db import models
from account.models import Account
# Create your models here.

class Address(models.Model):
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50,blank=True)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=50,blank=True)
    country = models.CharField(max_length=50,blank=True)
    state = models.CharField(max_length=50,blank=True)
    city = models.CharField(max_length=50,blank=True)
    pincode = models.CharField(max_length=50,blank=True)
    order_note = models.CharField(max_length=100, blank=True ,null=True)
    newly_added = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}"