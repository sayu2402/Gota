from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from wishlist.models import Wishlist
from django.views.decorators.cache import cache_control
from django.http.response import JsonResponse
from products.models import Product
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from products.models  import Variation
# Create your views here.


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='loginpage')
def wishlist(request):
    wishlist = Wishlist.objects.filter(user = request.user)
    context = {
        'wishlist' : wishlist,
    }
    return render(request, 'wishlist/wishlist.html',context)

def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    current_user = request.user
    product_variations = []

    if current_user.is_authenticated:
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variations.append(variation)
                except Variation.DoesNotExist:
                    pass

        wishlist_item, created = Wishlist.objects.get_or_create(user=current_user, product=product)

        if created:
            wishlist_item.variations.add(*product_variations)
            wishlist_item.save()

            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse({'message': 'Item added to wishlist'}, status=200)
            else:
                return redirect('wishlist')  # Redirect to the wishlist page

        else:
            return JsonResponse({'message': 'Item is already in your wishlist'}, status=400)

    else:
        return JsonResponse({'message': 'You need to be logged in to add items to your wishlist'}, status=401)
    
    
@login_required
def add_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    color = request.POST.get('color')
    size = request.POST.get('size')

    variation = None
    if color and size:
        variation_color = Variation.objects.filter(
            product=product,
            variation_category='color',
            variation_value__iexact=color
        ).first()

        variation_size = Variation.objects.filter(
            product=product,
            variation_category='size',
            variation_value__iexact=size
        ).first()

        if variation_color and variation_size:
            # Create a list of variations to add
            variations_to_add = [variation_color, variation_size]

            # Create the wishlist item with variations
            wishlist_item, created = Wishlist.objects.get_or_create(
                user=request.user,
                product=product
            )

            # Add variations to the wishlist item
            wishlist_item.variations.add(*variations_to_add)

            return JsonResponse({"status": "success", "message": "Item added to wishlist with variations."})
        else:
            return JsonResponse({"status": "error", "message": "Invalid color or size."})
    else:
        # Handle case where either color or size is missing
        return JsonResponse({"status": "error", "message": "Both color and size are required."})



# Remove wishlist
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def delete_wishlist(request,product_id):
    #print(product_id,'entering delete')
    
    product_id = product_id
    Wishlist.objects.filter(user=request.user, product=product_id).delete()
    # if wishlist_items.exists():
    #     wishlist_items.delete()
    return redirect('wishlist')


