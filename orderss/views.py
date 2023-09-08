import datetime
from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Payment, Order, OrderProduct
from carts.models import CartItem
from .forms import OrderForm
from django.contrib import messages
from .models import Order , OrderProduct
from products.models import Product , Variation , ProductOffer
from dashboard.models import Address
from django.urls import reverse
from categories.models import CategoryOffer



def place_order(request, total=0, quantity=0):
    
    current_user = request.user

    coupon_discount = request.session.get('coupon_discount', 0)
    # print(coupon_discount,"_____________")
    # Need to check if the cart is empty
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (18 * total) / 100
    grand_total = total + tax - coupon_discount


    if request.method == "POST":
        form = OrderForm(request.POST)
        
        if 'selected_address' in request.POST:
            # Address ID is provided, use the selected address
            selected_address_id = request.POST['selected_address']
            selected_address = Address.objects.get(pk=selected_address_id)

            # Create the order using the selected address data
            data = Order()
            data.user         = current_user
            data.first_name   = selected_address.first_name
            data.last_name    = selected_address.last_name
            data.phone        = selected_address.phone
            data.email        = selected_address.email
            data.address      = selected_address.address
            data.pincode      = selected_address.pincode
            data.country      = selected_address.country
            data.city         = selected_address.city
            data.order_total  = grand_total
            data.tax          = tax
            data.ip           = request.META.get('REMOTE_ADDR')
            data.save()

            # Delete the 'coupon_discount' session variable after order placement
            if 'coupon_discount' in request.session:
                del request.session['coupon_discount']
            for item in cart_items:
                product = Product.objects.get(id=item.product_id)

                # Create an OrderItem instance for each product in the order
                order_item = OrderProduct(
                    order=data,
                    user=current_user,
                    product=product,
                    quantity=item.quantity,
                    product_price=item.product.price * item.quantity
                )
                order_item.save()

                data.order_product = product  # Set the order_product field
                data.save()

                product.stock -= item.quantity
                product.save()

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            CartItem.objects.filter(user=current_user).delete()
            
            # Return a JSON response when using Razorpay mode
            if 'razorpay_mode' in request.POST:
                response_data = {
                    'message': 'Order placed successfully in Razorpay mode.',
                    'order_id':data.id
                }
                return JsonResponse(response_data)
            else:
                return redirect('checkout_confirmation')


        elif form.is_valid():
            # Create a new Address instance and populate it with the form data
            address_data    = Address(
                user        =  current_user,
                first_name  =  form.cleaned_data['first_name'],
                last_name   =  form.cleaned_data['last_name'],
                phone       =  form.cleaned_data['phone'],
                email       =  form.cleaned_data['email'],
                address     =  form.cleaned_data['address'],
                pincode     =  form.cleaned_data['pincode'],
                country     =  form.cleaned_data['country'],
                city        =  form.cleaned_data['city']
            )
            address_data.save()

            data = Order()
            data.user            = current_user
            data.first_name      = form.cleaned_data['first_name']
            data.last_name       = form.cleaned_data['last_name']
            data.phone           = form.cleaned_data['phone']
            data.email           = form.cleaned_data['email']
            data.address         = form.cleaned_data['address']
            data.company         = form.cleaned_data['company']
            data.pincode         = form.cleaned_data['pincode']
            data.country         = form.cleaned_data['country']
            data.city            = form.cleaned_data['city']
            data.order_total     = grand_total
            data.tax             = tax
            data.ip              = request.META.get('REMOTE_ADDR')
            data.save()


            # Delete the 'coupon_discount' session variable after order placement
            if 'coupon_discount' in request.session:
                del request.session['coupon_discount']

            # for deleting cart item after place order
            for item in cart_items:
                product = Product.objects.get(id=item.product_id)

                # Create an OrderItem instance for each product in the order
                order_item = OrderProduct(
                    order=data,
                    user=current_user,
                    product=product,
                    quantity=item.quantity,
                    product_price=item.product.price * item.quantity
                )
                order_item.save()

                data.order_product = product  # Set the order_product field
                data.save()

                product.stock -= item.quantity
                product.save()

            # creating a order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d  = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            CartItem.objects.filter(user=current_user).delete()
            
            # Return a JSON response when using Razorpay mode
            if 'razorpay_mode' in request.POST:
                response_data = {
                    'message': 'Order placed successfully in Razorpay mode.',
                    'order_id':data.id
                }
                return JsonResponse(response_data)
            else:
                return redirect('checkout_confirmation')


        else:
            # print("Form is not valid:", form.errors)
            # print("Form data:", form.data)
            return redirect('checkout')
    else:
        form = OrderForm()

    context = {
        'form': form,
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'userlist': Address.objects.filter(user=current_user),
    }
    return render(request, 'cart/checkout.html', context)


# for passing the grand_total to js
def payment(request, total = 0, quantity =0, cart_items = None):
    # for getting coupon discount that saved in session
    coupon_discount = request.session.get('coupon_discount', 0)

    user = request.user
    cart = CartItem.objects.filter(user=request.user)
    tax = 0
    grand_total = 0
    for item in cart:
        total += (item.product.price * item.quantity)
        quantity += item.quantity
    tax = (18 * total) / 100
    grand_total = total + tax - coupon_discount
    #print("grand_total :", grand_total)
    return JsonResponse({
        'grand_total': grand_total
    })


def order_list(request):
    orders = Order.objects.select_related('order_product').order_by('-created_at')
    order_status_choices = Order.STATUS
    return render(request, 'order/order_list.html', {'orders': orders, 'order_status_choices': order_status_choices})




def cancel_order(request,order_id):
    order = get_object_or_404(Order, id=order_id)

     # Update the order status to "Cancelled"
    order.status = 'Cancelled'
    order.save()
    messages.success(request,'Order has been cancelled successfully.')

    return redirect('order_list')


#admin user list
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        order.status = new_status
        order.save()
        messages.success(request,'Order status has been changed successfully.')

    return redirect('order_list')


def calculate_order_discount(order):
    total_discount = Decimal('0.00')

    # Iterate over order products and calculate product discounts
    for order_product in order.orderproduct_set.all():
        product = order_product.product
        product_offer = ProductOffer.objects.filter(product=product).filter(start_date__lte=order.created_at, end_date__gte=order.created_at).first()

        if product_offer:
            product_discount_percent = Decimal(product_offer.off_percent)  # Convert to Decimal
            product_discount_amount = (product_discount_percent / 100) * Decimal(order_product.product_price)  # Convert to Decimal
            total_discount += product_discount_amount

    # Iterate over order products and calculate category discounts
    for order_product in order.orderproduct_set.all():
        product = order_product.product
        category = product.category
        category_offer = CategoryOffer.objects.filter(category=category).filter(start_date__lte=order.created_at, end_date__gte=order.created_at).first()

        if category_offer:
            category_discount_percent = Decimal(category_offer.off_percent)  # Convert to Decimal
            category_discount_amount = (category_discount_percent / 100) * Decimal(order_product.product_price)  # Convert to Decimal
            total_discount += category_discount_amount

    return total_discount


def user_order_detail(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at').select_related('order_product')

    order_products = []

    for order in user_orders:
        product = order.order_product
        order_products.append(product)

        # Calculate the total discount for the order
        order.total_discount = calculate_order_discount(order)

        # Calculate the discounted total
        order.discounted_total = Decimal(order.order_total) - order.total_discount  # Convert to Decimal

    orders_count = user_orders.count()

    context = {
        'orders': user_orders,
        'orders_count': orders_count,
        'order_products': order_products,
    }

    return render(request, 'order/user_order_list.html', context)


def get_order_details(request, order_id):
    try:
        order = Order.objects.get(id=order_id)

        order_details = {
            'order_id': order.id,
            'order_date': order.created_at.strftime('%Y-%m-%d'),
        }

        return JsonResponse(order_details)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
    


# for cancel user order 
def cancel_order_user(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # print("Order ID received:", order_id)

    # print("Order status:", order.status)

    if order.status == 'New' or 'shipped':
        # print("Cancelling the order...")
        order.status = 'Cancelled'
        order.save()
        messages.success(request, 'Order has been cancelled successfully.')
    else:
        messages.error(request, 'Order cannot be cancelled.')

    return redirect('user_order_detail')


#Order details in admin side 
def admin_order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_products = OrderProduct.objects.filter(order=order)
    # print("Order :",order)
    context = {
        'order': order,
        'order_products' : order_products,
    }
    print(context)
    return render(request, 'order/admin_order_details.html', context)


# for user to view detail of their order
def user_view_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_products = OrderProduct.objects.filter(order=order)
    
    total_discount = Decimal('0.00')  # Initialize total discount to zero

    for order_product in order_products:
        product = order_product.product

        # Retrieve the applied product offer (if any)
        product_offer = ProductOffer.objects.filter(product=product).filter(start_date__lte=order.created_at, end_date__gte=order.created_at).first()
        if product_offer:
            product_discount_percent = Decimal(product_offer.off_percent)
            product_discount_amount = (product_discount_percent / 100) * Decimal(order_product.product_price)
            total_discount += product_discount_amount

        # Retrieve the applied category offer (if any)
        category = product.category
        category_offer = CategoryOffer.objects.filter(category=category).filter(start_date__lte=order.created_at, end_date__gte=order.created_at).first()
        if category_offer:
            category_discount_percent = Decimal(category_offer.off_percent)
            category_discount_amount = (category_discount_percent / 100) * Decimal(order_product.product_price)
            total_discount += category_discount_amount

    # Calculate the discounted total
    discounted_total = Decimal(order.order_total) - total_discount
    # print("________________", discounted_total)

    context = {
        'order': order,
        'order_products': order_products,
        'discounted_total': discounted_total,  # Pass the discounted total to the template
    }

    return render(request, 'order/user_view_order.html', context)