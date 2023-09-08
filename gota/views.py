from django.shortcuts import redirect, render
from django.views.decorators.cache import cache_control
from products.models import Product
from django.views.decorators.csrf import csrf_protect
from orderss.models import OrderProduct
from django.db.models import Count
from products.models import ProductOffer



@csrf_protect
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def home(request):
    #latest 2 products that added
    last_added_products = Product.objects.filter(is_available=True).order_by('-created_date')[:2]
    #most expensive product from the website
    most_expensive_shoes = Product.objects.filter(is_available=True).order_by('-price')[:2]
    #most ordered product from the website
    most_ordered_products = OrderProduct.objects.annotate(total_ordered=Count('id')).order_by('-total_ordered')[:3]
    #latest product offer 
    last_product_offer = ProductOffer.objects.order_by('-start_date').first()

    context = {
        'last_added_products' : last_added_products,
        'most_ordered_products' : most_ordered_products,
        'last_product_offer' : last_product_offer,
        'most_expensive_shoes' : most_expensive_shoes,
    }
    # print(last_added_products,"_________________")
    return render(request, 'home.html' , context)
