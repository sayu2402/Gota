from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Enter Email',
        'class': 'form-control',
    }))

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
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'form-control',
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@gmail.com'):
            raise forms.ValidationError('Invalid email format. Please enter a valid Gmail address.')
        return email

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Password does not match!')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class OTPVerificationForm(forms.Form):
    otp = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder': 'Enter OTP',
        'class': 'form-control',
    }), required=True)
