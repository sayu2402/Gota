from django import forms
from .models import Product , Category , ProductOffer
from .models import Variation , variation_category_choice


class ProductForm(forms.ModelForm):

    product_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Product name',
        'class': 'form-control',
        
    }))

    description = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Enter Description here',
        'class': 'form-control',
    }))

    price = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter price here',
        'class': 'form-control',
    }))

    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={
        'class': 'form-control-file',
    }))

    stock = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder': 'Enter stock quantity',
        'class': 'form-control',
    }))


    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control',
    }))


    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock < 0:
            raise forms.ValidationError("Stock quantity cannot be negative.")
        return stock
    
    class Meta:
        model = Product
        fields = ['product_name', 'description', 'price', 'images', 'stock', 'is_available', 'category']



class VariationForm(forms.ModelForm):

    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    variation_category = forms.ChoiceField(
        choices=variation_category_choice,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    variation_value = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    is_active = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    class Meta:
        model = Variation
        fields = ['product','variation_category', 'variation_value', 'is_active']



class ProductOfferForm(forms.ModelForm):
    class Meta:
        model = ProductOffer
        fields = ['product', 'name', 'off_percent', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }