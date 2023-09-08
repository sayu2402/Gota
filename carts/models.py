from django.db import models
from products.models import Product, Variation, Coupon
from account.models import Account

class Cart(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    cart_id = models.CharField(max_length=250, blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def get_cart_total(self):
        cart_items = self.cartitems.all()
        total = 0
        quantity = 0  # Initialize quantity to 0
        price = []  # Initialize an empty list to store individual item prices

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            price.append(cart_item.product.price * cart_item.quantity)  # Add individual item prices to the list

        tax = (18 * total) / 100
        grand_total = total + tax

        if self.coupon:  # Check if a coupon is applied
            return sum(price) - self.coupon.discount_price  # Apply coupon discount

        return grand_total

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cartitems")
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    coupons = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return str(self.product)
