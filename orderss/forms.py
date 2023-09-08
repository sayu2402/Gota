from django import forms
from .models import Order
from django.core.exceptions import ValidationError


class OrderForm(forms.ModelForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter First Name',
        'class': 'form-control',
        'pattern': '[A-Za-z]+',
        'title': 'Please enter alphabetic characters only',
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Last Name',
        'class': 'form-control',
        'pattern': '[A-Za-z]+',
        'title': 'Please enter alphabetic characters only',
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Enter Email',
        'class': 'form-control',
    }))

    phone = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter Your Phone Number',
        'class' : 'form-control'
    }))

    address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter Your Address',
        'class' : 'form-control'
    }))

    company = forms.CharField(
        required=False,  # This makes the field optional
        widget=forms.TextInput(attrs={
        'placeholder' : 'Enter Your Company Address(optional)',
        'class' : 'form-control'
    }))

    pincode = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter Your Pin Number',
            'class': 'form-control',
            'pattern': r'\d{6}',
            'title': 'Please enter a 6-digit numeric PIN.',
        }),
        label="Pincode",
        min_value=100000,  # Minimum 6-digit number
        max_value=999999,  # Maximum 6-digit number
        required=True,
    )



    country = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter Your Country Name',
        'class' : 'form-control'
    }))

    city = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter City Name',
        'class' : 'form-control'
    }))

    order_note = forms.CharField(
    required=False,  # This makes the field optional
    widget=forms.TextInput(attrs={
        'placeholder': 'Note about your order, e.g special note for delivery',
        'class': 'form-control'
    })
)



    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'company', 'address', 'city', 'country', 'pincode', 'phone', 'email','order_note']


    def clean_pincode(self):
        pincode = self.cleaned_data['pincode']
        if len(str(pincode)) != 6:
            raise ValidationError('Pincode should be exactly 6 digits long.')
        return pincode
    


    


    