from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import CategoryForm , CategoryOfferForm
from .models import Category
from django.shortcuts import render, get_object_or_404
from .models import Category , CategoryOffer
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from products.models import Product
from django.contrib import messages



@login_required(login_url='loginpage')
def add_categories(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)                   # Get the form data without saving it yet
            if not category.slug:                                # Check if the slug is empty
                category.slug = slugify(category.category_name)  # Generate the slug
            category.save()                                      # Now save the category with the generated or custom slug
            return redirect('admin_categories')
    else:
        form = CategoryForm()

    return render(request, 'category/add_categories.html', {'form': form})


def admin_categories(request):
    categories = Category.objects.all()
    return render(request, 'category/admin_categories.html', {'categories': categories})



@login_required(login_url='loginpage')
def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('admin_categories')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'category/category_detail.html', {'form': form})


@login_required(login_url='loginpage')
def category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        category.delete()
        return redirect('admin_categories')

    return render(request, 'category/category_confirm_delete.html', {'category': category})


#<---------------------------------------------------Category Offer Start---------------------------------------------------------->

def add_category_offer(request):
    category_offers = CategoryOffer.objects.all()

    if request.method == 'POST':
        form = CategoryOfferForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category offer added successfully.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = CategoryOfferForm()

    context = {
        'category_offers': category_offers,
        'form': form,
    }
    return render(request, 'category/add_category_offer.html', context)



def edit_category_offer(request, offer_id):
    offer = get_object_or_404(CategoryOffer, id=offer_id)

    if request.method == 'POST':
        form = CategoryOfferForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category offer updated successfully.')
            return redirect('add_category_offer')
    else:
        form = CategoryOfferForm(instance=offer)

    context = {
        'form': form,
        'offer': offer,
    }
    return render(request, 'category/edit_category_offer.html', context)



def delete_category_offer(request, offer_id):
    offer = get_object_or_404(CategoryOffer, id=offer_id)

    if request.method == 'POST':
        offer.delete()
        messages.success(request, 'category offer deleted successfully.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


#<-----------------------------------------------Category offer End --------------------------------------------------------->