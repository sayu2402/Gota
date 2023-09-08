from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import redirect, render , get_object_or_404
from django.views.decorators.cache import cache_control
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from carts.models import Cart, CartItem
from carts.views import _cart_id
from products.models import Product , ProductOffer
from orderss.models  import Order , OrderProduct
from django.contrib import messages
from .models import Address
from account.models import Account
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from orderss.forms import OrderForm
from .forms import AddressForm
from categories.models import Category
from django.db.models import Sum
from django.utils import timezone
from datetime import date, datetime, timedelta
import datetime
import calendar
from django.db.models import Count
from django.template.loader import get_template
from xhtml2pdf import pisa
from orderss.models import Order
from categories.models import CategoryOffer




# Create your views here.

#user dashboard
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id = request.user.id)
    userlist = Address.objects.filter(user=request.user)
    orders_count = orders.count()
    context = {
        'orders_count' : orders_count,
        'userlist' : userlist,
    }
    return render(request, 'dashboard/user_dashboard.html' , context)


#add address from user dashboard
def add_address(request):

    if request.method == 'POST':

        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        country=request.POST.get('country')
        address=request.POST.get('address')
        city=request.POST.get('city')
        pincode=request.POST.get('pincode')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        state=request.POST.get('state')
        order_note=request.POST.get('order_note')


        if request.user is None:
            return
        
        if first_name.strip() == '' or last_name.strip() == '':
            messages.error(request,'names cannot be empty!!!')
            return redirect('dashboard')
        
        if country.strip()=='':
            messages.error(request,'Country cannot be empty')
            return redirect('dashboard')
        if city.strip()=='':
            messages.error(request,'city cannot be empty')
            return redirect('dashboard')
        if address.strip()=='':
            messages.error(request,'address cannot be empty')
            return redirect('dashboard')
        if pincode.strip()=='':
            messages.error(request,'pincode cannot be empty')
            return redirect('dashboard')
        if phone.strip()=='':
            messages.error(request,'phone cannot be empty')
            return redirect('dashboard')
        if email.strip()=='':
            messages.error(request,'email cannot be empty')
            return redirect('dashboard')
        if state.strip()=='':
            messages.error(request,'state cannot be empty')
            return redirect('dashboard')

        ads=Address()
        ads.user=request.user
        ads.first_name=first_name
        ads.last_name=last_name
        ads.country=country
        ads.address=address
        ads.city=city
        ads.pincode=pincode
        ads.phone=phone
        ads.email=email
        ads.state=state
        ads.order_note=order_note
        ads.save()

        return redirect('dashboard')
    

def edit_address(request,edit_id):

    if request.method == 'POST':

        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        country=request.POST.get('country')
        address=request.POST.get('address')
        city=request.POST.get('city')
        pincode=request.POST.get('pincode')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        state=request.POST.get('state')
        order_note=request.POST.get('order_note')


        if request.user is None:
            return
        
        if first_name.strip() == '' or last_name.strip() == '':
            messages.error(request,'names cannot be empty!!!')
            return redirect('dashboard')
        
        if country.strip()=='':
            messages.error(request,'Country cannot be empty')
            return redirect('dashboard')
        if city.strip()=='':
            messages.error(request,'city cannot be empty')
            return redirect('dashboard')
        if address.strip()=='':
            messages.error(request,'address cannot be empty')
            return redirect('dashboard')
        if pincode.strip()=='':
            messages.error(request,'pincode cannot be empty')
            return redirect('dashboard')
        if phone.strip()=='':
            messages.error(request,'phone cannot be empty')
            return redirect('dashboard')
        if email.strip()=='':
            messages.error(request,'email cannot be empty')
            return redirect('dashboard')
        if state.strip()=='':
            messages.error(request,'state cannot be empty')
            return redirect('dashboard')

        try:
            ads = Address.objects.get(id=edit_id)
        except Address.DoesNotExist:
            messages.error(request, 'Address not found')
            return redirect('dashboard')
        ads.user=request.user
        ads.first_name=first_name
        ads.last_name=last_name
        ads.country=country
        ads.address=address
        ads.city=city
        ads.pincode=pincode
        ads.phone=phone
        ads.email=email
        ads.state=state
        ads.order_note=order_note
        ads.save()

        return redirect('dashboard')
    else:
        return redirect('dashboard')
    

def editprofile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
 

        if username == '':
            messages.error(request, 'Username is empty')
            return redirect('dashboard')
        if first_name == '' or last_name == '':
            messages.error(request, 'First or Lastname is empty')
            return redirect('dashboard')
      
        try:
            user = Account.objects.get(username=request.user)
            # print(user)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email=email
            user.save()
            messages.success(request, 'userprofile updated successfully')
        except ObjectDoesNotExist:
            messages.error(request, 'User does not exist')
    return redirect('user_profile')


# Change Password from user dashboard
def changepassword(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        # Validation
        if new_password != confirm_new_password:
            messages.error(request, 'Password did not match')
            return redirect('dashboard')

        try:
            user = Account.objects.get(username=request.user.username)
        except Account.DoesNotExist:
            return redirect('dashboard')  # Handle the case if the user doesn't exist

        if check_password(old_password, user.password):
            user.set_password(new_password)
            user.save()

            update_session_auth_hash(request, user)

            messages.success(request, 'Password updated successfully')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid old password')
            return redirect('dashboard')

    return redirect('dashboard')


# delete Address
def deleteaddress(request,delete_id):
    address = Address.objects.get(id = delete_id)
    address.delete()
    return redirect('dashboard')


from datetime import datetime, timedelta
@login_required(login_url='loginpage')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_dashboard(request):
    # Calculate monthly orders
    today = datetime.today()
    last_day_of_month = calendar.monthrange(today.year, today.month)[1]

    start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_month = today.replace(day=last_day_of_month, hour=23, minute=59, second=59, microsecond=999999)

    orders = Order.objects.select_related('order_product', 'user').order_by('-created_at')
    total_revenue = orders.aggregate(Sum('order_total'))['order_total__sum']
    if total_revenue is not None:
        total_revenue = round(total_revenue, 2)

    # for calculating monthly orders
    monthly_orders = orders.filter(
        created_at__gte=start_of_month,
        created_at__lt=end_of_month
    )
    monthly_revenues = monthly_orders.aggregate(Sum('order_total'))['order_total__sum']
    if monthly_revenues is not None:
        monthly_revenues = round(monthly_revenues, 2)
    else:
        monthly_revenues = 0
    # print("_________________", monthly_revenues)

    # to find total orders
    total_orders = Order.objects.count()  

    # to find total products
    total_products = Product.objects.count()  

    # to find total no.of categories
    total_categories = Category.objects.count() 

    # Get the 5 most recent orders for recent activities
    recent_activities = orders[:4]  

    # to find last 3 joined users
    new_members = Account.objects.order_by('-date_joined')[:3] 

    # to find last 5 orders
    recent_orders = orders.select_related('user').filter(status='Delivered').order_by('-created_at')[:5]  

    # Calculate the top selling categories and their percentages
    categories_sales = Category.objects.annotate(total_sales=Count('product__order__id')).order_by('-total_sales')
    top_categories = []
    for category in categories_sales:
        category_percentage = (category.total_sales / total_orders) * 100
        top_categories.append({
            'name': category.category_name,
            'percentage': round(category_percentage),
        })

    # Calculate monthly sales data for line chart
    today = datetime.today()
    monthly_sales_data = []

    for month in range(1, 13):
        last_day_of_month = calendar.monthrange(today.year, month)[1]
        start_of_month = today.replace(day=1, month=month, hour=0, minute=0, second=0, microsecond=0)
        end_of_month = today.replace(day=last_day_of_month, month=month, hour=23, minute=59, second=59, microsecond=999999)

        # Calculate sales for this month (replace this with your actual sales calculation logic)
        monthly_orders = orders.filter(
            created_at__gte=start_of_month,
            created_at__lte=end_of_month
        )
        monthly_revenue = monthly_orders.aggregate(Sum('order_total'))['order_total__sum']
        if monthly_revenue is not None:
            monthly_revenue = round(monthly_revenue, 2)
        else:
            monthly_revenue = 0

        monthly_sales_data.append(monthly_revenue)
    

    # Calculate order status counts for pie chart
    cancelled_count = Order.objects.filter(status='Cancelled').count()
    delivered_count = Order.objects.filter(status='Delivered').count()
    shipped_count = Order.objects.filter(status='Shipped').count()
    new_count = Order.objects.filter(status='New').count()

    context = {
        'total_orders': total_orders,
        'total_products': total_products,
        'total_categories': total_categories,
        'total_revenue': total_revenue,
        'monthly_revenue': monthly_revenues,
        'recent_activities': recent_activities,
        'new_members': new_members,
        'recent_orders': recent_orders,
        'top_categories': top_categories,
        'monthly_sales_data': monthly_sales_data,
        'cancelled_count': cancelled_count,
        'delivered_count': delivered_count,
        'shipped_count': shipped_count,
        'new_count': new_count,
    }
    # print(monthly_revenue,"_____________")
    return render(request, 'dashboard/admin_dashboard.html', context)



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def adminlogout(request):
    logout(request)
    return redirect('loginpage')



def add_new_adress(request):
    cart_items = None
    total = 0
    quantity = 0

    coupon_discount = request.session.get('coupon_discount', 0)
    category_discount = 0  # Initialize category discount to zero

    product_discount = 0

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
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

    new_address_info = []
    for address in Address.objects.filter(user=request.user):
        address_info = {
            'id': address.id,
            'first_name': address.first_name,
            'user': address.user.username,
            'phone': address.phone,
            'email': address.user.email,
            'address': address.address,
            'city': address.city,
        }
        new_address_info.append(address_info)

    for order in Order.objects.filter(user=request.user):
        order_info = {
            'id': order.id,
            'first_name': order.first_name,
            'user': order.user.username,
            'phone': order.phone,
            'email': order.user.email,
            'address': order.address,
            'city': order.city,
        }
        new_address_info.append(order_info)

    new_address_info.sort(key=lambda x: x['id'])

    formatted_grand_total = "{:.2f}".format(grand_total - coupon_discount - category_discount - product_discount) if cart_items else "Your Cart is Empty"

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': formatted_grand_total,
        'form': OrderForm(),
        'new_address_info': new_address_info,
        'coupon_discount': coupon_discount,
        'category_discount': category_discount,  # Add category discount to the context
    }

    return render(request, 'cart/checkout_new.html', context)


#To show confirmation message for the user
def checkout_confirmation(request):
    # Retrieve the latest order for the current user
    try:
        order = Order.objects.filter(user=request.user).latest('created_at')
    except Order.DoesNotExist:
        order = None

    context = {
        'order': order
    }

    return render(request, 'cart/checkout_confirmation.html', context)


#To edit adress from checkout Page
def edit_address_checkout(request, edit_id):
    address = get_object_or_404(Address, id=edit_id)

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('checkout')
    else:
        form = AddressForm(instance=address)

    context = {'form': form}
    return render(request, 'cart/user_edit.html', context)


#To delete address from checkout page
def delete_address_checkout(request, delete_id):
    # Get the address using the delete_id
    address = get_object_or_404(Address, pk=delete_id)

    # Check if the address belongs to the current user
    if request.user == address.user:
        # Delete the address
        address.delete()
        # Redirect back to the checkout page or any other desired page
        return redirect('checkout')
    else:
        # Redirect to an appropriate page with an error message
        return redirect('checkout')
    



#<---------------------------------------------For downloading Sales Report---------------------------------------------------->


#for generating sales report
def sales_report(request):
    if not request.user.is_superadmin:
        return redirect('admin_login')
   
    start_date = None
    end_date = None
    sales_lists = None
    
    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        report_type = request.POST.get('report_type')
        
        try:
            if start_date_str:
               start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            if end_date_str:
               end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
               end_date += timedelta(days=1)  # Add one day to include the entire last day
               end_date -= timedelta(seconds=1)
            
            if start_date and end_date:
                sales_lists = Order.objects.filter(created_at__range=[start_date, end_date], status='Delivered')
            elif not start_date and not end_date:
                sales_lists = Order.objects.filter(status='Delivered') 
                
            if report_type == 'pdf':
                return generate_pdf_report(sales_lists)
            elif report_type == 'csv':
                return generate_csv_report(sales_lists)
        except ValueError:
            error_message = "Invalid date format. Please use YYYY-MM-DD."
            return render(request, 'sales/sales.html', {'error_message': error_message})
    else:
        sales_lists = Order.objects.filter(status='Accepted') 
    return render(request, 'sales/sales.html', {'sales_lists': sales_lists})



def generate_pdf_report(sales_lists):
    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'

    # Generate the PDF content using the xhtml2pdf library
    template_path = 'sales/sales_report_template.html'
    context = {'sales_lists': sales_lists}
    template = get_template(template_path)
    html = template.render(context)
    pdf = pisa.pisaDocument(html, response)

    if not pdf.err:
        return response
    return HttpResponse('Error generating PDF')

import csv

def generate_csv_report(sales_lists):
    # Create a CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'

    # Write CSV data
    writer = csv.writer(response)
    writer.writerow(['Order Number', 'Customer', 'Created At', 'Total'])
    
    for sale in sales_lists:
        writer.writerow([sale.order_number, sale.user.username, sale.created_at, sale.order_total])

    return response


#<--------------------------------------------------------End Sales Report ------------------------------------------------------------------->



#<-----------------------------------------------User Invoice-------------------------------------------------------->

#user side invoice download
def generate_pdf(request, order_id):
    coupon_discount = request.session.get('coupon_discount', 0)

    print("Coupon Discount:", coupon_discount)

    # Fetch the order and its associated order_products
    order = get_object_or_404(Order, id=order_id)
    order_products = OrderProduct.objects.filter(order=order)

    total_price = sum(order_product.product_price for order_product in order_products)

    # Calculate the discounts based on active and non-expired category and product offers
    category_discount = 0
    product_discount = 0

    for order_product in order_products:
        # Check if the product's category has an active category offer
        category_offer = None
        try:
            category_offer = CategoryOffer.objects.get(category=order_product.product.category)
            if category_offer.end_date < date.today():
                category_offer = None  # Expired offer, ignore it
        except CategoryOffer.DoesNotExist:
            pass

        if category_offer:
            # Apply category-specific discount to the total
            if category_offer.off_percent > 0:
                category_discount += (order_product.product_price * order_product.quantity) * (
                    category_offer.off_percent / 100)

        # Check if the product has an active product offer
        product_offer = None
        try:
            product_offer = ProductOffer.objects.get(product=order_product.product)
            if product_offer.end_date < date.today():
                product_offer = None  # Expired offer, ignore it
        except ProductOffer.DoesNotExist:
            pass

        if product_offer:
            # Apply product-specific discount to the total
            if product_offer.off_percent > 0:
                product_discount += (order_product.product_price * order_product.quantity) * (
                    product_offer.off_percent / 100)

    # Calculate the total price after discounts
    total_price_after_discounts = (order.order_total) - category_discount - product_discount

    # Load the PDF template
    template_path = 'sales/invoice_user.html'  # Replace with the actual path
    template = get_template(template_path)

    # Prepare the template context
    context = {
        'order': order,
        'order_products': order_products,
        'total_price' : total_price,
        'product_discount': product_discount,  
        'category_discount': category_discount,
        'total_price_after_discounts': total_price_after_discounts,
        'coupon_discount' : coupon_discount,
    }

    # Render the template to HTML
    html = template.render(context)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.order_number}.pdf"'

    # Generate the PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Check if PDF generation was successful
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)

    return response


#<--------------------------------------------------------User Invoice End------------------------------------------------------------->