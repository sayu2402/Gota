from django.db import models
from products.models import Product , Variation
from account.models import Account

# Create your models here.

class Wishlist(models.Model):
    user        =  models.ForeignKey(Account, on_delete=models.CASCADE)
    product     =  models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    variations  = models.ManyToManyField(Variation, blank=True)


    def __str__(self):
        return f'{self.user.username} Wishlist'

    def total_quantity(self):
        return self.variations.count()
