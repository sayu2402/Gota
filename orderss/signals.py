from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from carts.models import CartItem

@receiver(post_save, sender=Order)
def delete_cart_items(sender, instance, **kwargs):
    if instance.status == 'Placed':
        cart_items = CartItem.objects.filter(user=instance.user)
        cart_items.delete()
