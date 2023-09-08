from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from products.models import Product , Variation , Coupon
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from orderss.forms import OrderForm
from dashboard.models import Address
from orderss.models import Order
from django.contrib import messages
from .forms import CouponForm
from categories.models import CategoryOffer
from products.models import ProductOffer
from datetime import date

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart



def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    
    if current_user.is_authenticated:
        product_variation = []
    
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()


        if not is_cart_item_exists:
            product.stock -= 1
            product.save()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            
            ex_var_list = []
            id = []  # list of cart_item id
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
                product.stock -= 1
                product.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()

            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse({'message': 'Quantity increased successfully'}, status=200)
            else:
                return redirect('cart')

        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()

            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse({'message': 'Item added to cart'}, status=200)
            else:
                return redirect('cart')
        
    else:
        product_variation = []
        
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
        
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)

            ex_var_list = []
            id = []  # list of cart_item id
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()

            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse({'message': 'Quantity increased successfully'}, status=200)
            else:
                return redirect('cart')

        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()

            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'quantity': cart_item.quantity}, status=200)
            else:
                return redirect('cart')


# for decreasing cart quantity
def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            product.stock += 1
            product.save()
        else:
            cart_item.delete()
        
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'quantity': cart_item.quantity}, status=200)
        else:
            return redirect('cart')


    except ObjectDoesNotExist:
        pass
    
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    context = {}
    couponss = Coupon.objects.all().order_by('is_expired')
    cart = None

    try:
        tax = 0
        grand_total = 0
        category_discount = 0
        product_discount = 0
        coupon_discount = 0  # Initialize coupon discount to zero

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        # Calculate cart totals
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

            # Check if the product's category has an active category offer
            category_offer = None
            try:
                category_offer = CategoryOffer.objects.get(category=cart_item.product.category)
                if category_offer.end_date < date.today():
                    category_offer = None  # Expired offer, ignore it
            except CategoryOffer.DoesNotExist:
                pass

            if category_offer:
                # Apply category-specific discount to the total
                if category_offer.off_percent > 0:
                    category_discount += (cart_item.product.price * cart_item.quantity) * (
                        category_offer.off_percent / 100)

            # Check if the product has an active product offer and is not expired
            product_offer = None
            try:
                product_offer = ProductOffer.objects.get(product=cart_item.product)
                if product_offer.end_date < date.today():
                    product_offer = None  # Expired offer, ignore it
            except ProductOffer.DoesNotExist:
                pass

            if product_offer:
                if product_offer.off_percent > 0:
                    product_discount += (cart_item.product.price * cart_item.quantity) * (
                        product_offer.off_percent / 100)

        tax = (18 * total) / 100
        grand_total = total + tax - category_discount - product_discount

        if request.method == 'POST':
            coupon_code = request.POST.get('coupon_code')
            try:
                coupon_obj = Coupon.objects.get(coupon_code__iexact=coupon_code)

                if coupon_obj.is_expired:
                    messages.error(request, "Coupon already Expired")
                    return redirect('cart')

                if coupon_obj.minimum_amount > grand_total:
                    messages.error(request, f'Amount should be greater than {coupon_obj.minimum_amount}')
                    return redirect('cart')

                for cart_item in cart_items:
                    if cart_item.coupons:
                        messages.error(request, 'Already Applied')
                        return redirect('cart')

                # Update the cart to associate it with the coupon
                if cart:
                    cart.coupon = coupon_obj
                    cart.save()

                coupon_discount = coupon_obj.discount_price
                grand_total -= coupon_discount

                # Store the coupon discount in the session
                request.session['coupon_discount'] = coupon_discount

                messages.success(request, 'Coupon applied successfully!')

            except Coupon.DoesNotExist:
                messages.warning(request, "Invalid coupon code")
                return redirect('cart')

        formatted_grand_total = "{:.2f}".format(grand_total)
        available_coupons = Coupon.objects.filter(is_expired=False, minimum_amount__lte=grand_total)
        context = {
            'total': total,
            'quantity': quantity,
            'cart_items': cart_items,
            'tax': tax,
            'grand_total': formatted_grand_total,
            'coupon_discount': coupon_discount,
            'category_discount': category_discount,
            'available_coupons': available_coupons,
            'couponss': couponss,
        }

    except ObjectDoesNotExist:
        pass

    return render(request, 'cart/cart.html', context)



# for deleting/removing cart item
def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    
    # Get the quantity of the cart item before deletion
    cart_item_quantity = cart_item.quantity

    cart_item.delete()
    
    # Delete the 'coupon_discount' session variable after order placement
    if 'coupon_discount' in request.session:
        del request.session['coupon_discount']
    
    # Update the product stock
    product.stock += cart_item_quantity
    product.save()
    
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        response_data = {'message': 'Item removed from cart'}
        return JsonResponse(response_data)
    
    return redirect('cart')



@login_required(login_url='loginpage')
def checkout(request, total=0, quantity=0, cart_items=None):
    userlist = Address.objects.filter(user=request.user)

    # Retrieve the coupon discount from the session
    coupon_discount = request.session.get('coupon_discount', 0)  # Retrieve the coupon discount

    # Initialize category discount to zero
    category_discount = 0

    product_discount = 0

    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

            # Check if the product's category has an active category offer
            category_offer = None
            try:
                category_offer = CategoryOffer.objects.get(category=cart_item.product.category)
                if category_offer.end_date < date.today():
                    category_offer = None  # Expired offer, ignore it
            except CategoryOffer.DoesNotExist:
                pass

            if category_offer:
                # Apply category-specific discount to the total
                if category_offer.off_percent > 0:
                    category_discount += (cart_item.product.price * cart_item.quantity) * (
                        category_offer.off_percent / 100)
            

            # Check if the product has an active product offer and is not expired
            product_offer = None
            try:
                product_offer = ProductOffer.objects.get(product=cart_item.product)
                if product_offer.end_date < date.today():
                    product_offer = None  # Expired offer, ignore it
            except ProductOffer.DoesNotExist:
                pass

            if product_offer:
                if product_offer.off_percent > 0:
                    product_discount += (cart_item.product.price * cart_item.quantity) * (
                        product_offer.off_percent / 100)


        tax = (18 * total) / 100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    new_address_info = Address.objects.filter(user=request.user)
    # print("___________",new_address_info)

    formatted_grand_total = "{:.2f}".format(grand_total - coupon_discount - category_discount - product_discount)
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': formatted_grand_total,
        'form': OrderForm(),
        'userlist': userlist,
        'new_address_info': new_address_info,
        'coupon_discount': coupon_discount,
        'category_discount': category_discount,  # Add category discount to the context
    }
    return render(request, 'cart/checkout.html', context)



def update_quantity(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        item_id = request.POST.get('item_id')
        new_quantity = int(request.POST.get('new_quantity', 1))

        try:
            cart_item = get_object_or_404(CartItem, id=item_id)
            if new_quantity <= 0:
                cart_item.delete()
            else:
                cart_item.quantity = new_quantity
                cart_item.save()
                messages.success(request, 'Product added to the cart.')

            # Recalculate the sub-total and cart total
            item_sub_total = cart_item.product.price * cart_item.quantity

            cart = cart_item.cart
            cart_items = cart.cartitem_set.filter(is_active=True) 
            cart_total = sum(item.product.price * item.quantity for item in cart_items)

            return JsonResponse({
                'success': True,
                'item_sub_total': item_sub_total,
                'cart_total': cart_total
            })
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})




# <----------------------------Coupon Management------------------------------->

# remove coupon from user side 
def remove_coupon(request, cart_id):
    cart = get_object_or_404(Cart, uid=cart_id)
    
    cart.coupon = None
    cart.save()
    
    # Remove the coupon_discount from the session
    if 'coupon_discount' in request.session:
        del request.session['coupon_discount']
    
    messages.success(request, "Coupon removed")
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def manage_coupons(request):
    coupons = Coupon.objects.all()

    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_coupons')
    else:
        form = CouponForm()

    context = {
        'coupons': coupons,
        'form': form,
    }
    return render(request, 'coupon/add_coupon.html', context)



def edit_coupon(request, coupon_id):
    coupon = Coupon.objects.get(pk=coupon_id)
    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            return redirect('manage_coupons')
    else:
        form = CouponForm(instance=coupon)

    context = {
        'form': form,
        'edit_coupon_id': coupon_id,
        'coupon': coupon,  # Pass the coupon instance for the modal
    }
    return render(request, 'coupon/edit_coupon.html', context)



def delete_coupon(request, coupon_id):
    coupon = Coupon.objects.get(pk=coupon_id)
    if request.method == 'POST':
        coupon.delete()
        return redirect('manage_coupons')

    context = {
        'coupon': coupon,
    }
    return render(request, 'coupon/delete_coupon.html', context)


# <--------------------------Coupon Management Ended------------------------------->