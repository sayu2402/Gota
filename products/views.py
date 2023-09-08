from django.http import HttpResponseRedirect
from django.shortcuts import render , redirect
from categories.models import Category
from .forms import ProductForm, VariationForm , ProductOfferForm
from .models import Product , Variation , ProductOffer
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
import requests
from categories.models import CategoryOffer
from django.db.models import Q

# Create your views here.

def admin_product_list(request):
    products = Product.objects.all()
    return render(request, 'product/admin_products.html', {'products': products})


def variation_list(request):
    variations = Variation.objects.select_related('product').all()
    context = {
        'variations': variations
    }
    return render(request, 'product/variation.html', context)



@login_required(login_url='loginpage')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        try:
            is_available_value = request.POST.get('checkbox', False)
            if is_available_value == 'on':
                is_available = True
            else:
                is_available = False
        except:
            is_available = False

        if form.is_valid():
            form.instance.is_available = is_available
            form.save()
            return redirect('admin_product_list')
    else:
        form = ProductForm()

    return render(request, 'product/add_product.html', {'form': form })




def store(request, category_slug=None):
    categories = None
    products = None

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
    else:
        products = Product.objects.all()

    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)
    elif min_price:
        products = products.filter(price__gte=min_price)
    elif max_price:
        products = products.filter(price__lte=max_price)

    # Sorting
    sorting = request.GET.get('sorting')
    if sorting == 'price_asc':
        products = products.order_by('price')
    elif sorting == 'price_desc':
        products = products.order_by('-price')
    elif sorting == 'name_asc':
        products = products.order_by('product_name')
    elif sorting == 'name_desc':
        products = products.order_by('-product_name')
    else:
        # Default to sorting by creation date (newest first)
        products = products.order_by('-created_date')

    # Get the associated ProductOffers for each product
    product_offers = ProductOffer.objects.filter(product__in=products)

    product_count = products.count()

    context = {
        'products': products,
        'product_offers': product_offers,
        'product_count': product_count,
        'category': categories,
    }

    return render(request, 'product/store.html', context)



@login_required(login_url='loginpage')
def product_edit(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES ,instance=product)
        if form.is_valid():
            form.save()
            # message
            return redirect('admin_product_list')
    else:
        form = ProductForm(instance=product)
    

    return render(request, 'product/product_edit.html', {'form': form})


@login_required(login_url='loginpage')
def product_delete(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)

    if request.method == 'POST':
        product.delete()
        
        return redirect('admin_product_list')

    return render(request, 'product/product_confirm_delete.html', {'product': product})



def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        category_offer = CategoryOffer.objects.filter(category=single_product.category).first()
        product_offer = ProductOffer.objects.filter(product=single_product).first()
        #print("_______________",category_offer)
    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product,
        'category_offer': category_offer,  # Pass the category offer to the template
        'product_offer' : product_offer,
    }
    #print("context product :" , context)
    return render(request, 'product/product_detail.html', context)


def add_variation(request):
    #print("Inside add_variation view")

    if request.method == 'POST':
        # print("POST request received")
        # print("POST data:", request.POST) 

        form = VariationForm(request.POST)

        try: # to handle checkbox exception
            is_available_value = request.POST.get('checkbox', False)
            if is_available_value == 'on':
                is_active = True
            else:
                is_active = False
        except:
            is_active = False

        if form.is_valid():
            # print("Form is valid")
            product = form.cleaned_data['product']
            
            # Create the variation instance and associate it with the product
            variation = form.save(commit=False)
            variation.product = product
            variation.save()

            # print("Variation saved")
            return redirect('variation_list')
        
        # else:
        #     print("Form is invalid:", form.errors)  # Print the form errors to the console
    else:
        form = VariationForm()

    return render(request, 'product/add_variation.html', {'form': form})


def update_is_active(request, variation_id):
    if request.method == 'POST':
        variation = Variation.objects.get(pk=variation_id)
        variation.is_active = not variation.is_active
        variation.save()
    return redirect('variation_list')


#<----------------------------------------------Offer Management----------------------------------------------------------->


def add_product_offer(request):
    product_offers = ProductOffer.objects.all()

    if request.method == 'POST':
        form = ProductOfferForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product offer added successfully.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = ProductOfferForm()

    context = {
        'product_offers': product_offers,
        'form': form,
    }
    return render(request, 'product/add_product_offer.html', context)



def edit_offer(request, offer_id):
    offer = get_object_or_404(ProductOffer, id=offer_id)

    if request.method == 'POST':
        form = ProductOfferForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product offer updated successfully.')
            return redirect('add_product_offer')
    else:
        form = ProductOfferForm(instance=offer)

    context = {
        'form': form,
        'offer': offer,
    }
    return render(request, 'product/edit_product_offer.html', context)



def delete_offer(request, offer_id):
    offer = get_object_or_404(ProductOffer, id=offer_id)

    if request.method == 'POST':
        offer.delete()
        messages.success(request, 'Product offer deleted successfully.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



#<---------------------------------------------End of Offer Management -------------------------------------------------------->


#<---------------------------------------------------Search Option------------------------------------------------------------->

# search for user side 
from django.db.models import Q

def search(request):
    products = []  # Initialize the products list
    product_count = 0

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword) |
                Q(category__category_name__icontains=keyword) 
            )
            product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'product/store.html', context)


#<----------------------------------------------------Search Option End------------------------------------------------------------>