import re
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib import messages , auth
from django.views.decorators.csrf import csrf_protect
from carts.models import Cart , CartItem
from .models import Account
from django.views.decorators.cache import cache_control
from django.shortcuts import redirect, get_object_or_404
from .forms import RegistrationForm, OTPVerificationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import random
from django.contrib import messages
from django.core.mail import send_mail
from .models import UserOTP
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from carts.views import _cart_id
import requests



def loginpage(request):
    if request.user.is_authenticated:
        if request.user.is_superadmin:
            return redirect('admin_dashboard')
        else:
            return redirect('home')
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        # print(f"Email: {email}, Password: {password}")
        user = auth.authenticate(email=email, password=password,)
        # print(f"Authenticated User: {user}")
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    #getting the product variation
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))
                    
                    # cart items from the user to acces product variation
                    cart_item = CartItem.objects.filter(user = user)
                    ex_var_list = []
                    id = [] # list of cart_item id
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr) #position of common item
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass

            if user.is_active and not user.is_blocked:
                auth.login(request, user)
                if user.is_superadmin:  
                    return redirect('admin_dashboard')
                else:
                    url = request.META.get('HTTP_REFERER')
                    try:
                        query = requests.utils.urlparse(url).query
                        # print('query -->', query) = # next=/cartscheckout/ --> want to split this url

                        params = dict(x.split('=') for x in query.split('&')) #splitting 

                        # print('params -->', params) = # {'next': '/cartscheckout/'}

                        if 'next' in params:
                            nextPage = params['next']
                            return redirect(nextPage)
                    except:
                        return redirect('dashboard')
                    
            else:
                messages.error(request, 'Invalid Email or Password')
        else:
            messages.error(request, 'Invalid Email or Password')
    return render(request, 'accounts/loginpage.html')


@csrf_protect
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        get_otp = request.POST.get('otp')

        # print(get_otp,'---------------------------')

        if get_otp:
            get_email = request.POST.get('email')
            
            # print(f"get_email: {get_email}")

            if not get_email:
                return render(request, 'accounts/signup.html')
            

            usr = get_object_or_404(Account, email=get_email)

            if int(get_otp) == UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active = True
                usr.save()
                login(request, usr , backend='django.contrib.auth.backends.ModelBackend')
                UserOTP.objects.filter(user=usr).delete()
                return redirect('home')
            else:
                messages.warning(request, 'You entered a wrong OTP')
                return render(request, 'accounts/otp_validation.html', {'email': get_email})
        else:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                firstname = form.cleaned_data['first_name']
                lastname = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']

                # Create a new user
                user = form.save(commit=False)
                user.username = email.split('@')[0]
                user.set_password(password)
                user.is_active = False
                user.save()

                # Generate and save OTP
                user_otp = random.randint(100000, 999999)
                UserOTP.objects.create(user=user, otp=user_otp)

                # Send verification email with OTP
                mess = f'Hello {user.username},\nYour OTP to verify your account for Gota is {user_otp}\n Thanks You!'
                send_mail(
                    "Welcome to Gota Shoes, verify your Email",
                    mess,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False
                )

                messages.success(request, 'Registration Successful. Check your email for OTP verification.')
                # return redirect('otp_validation', email=email)
                return HttpResponseRedirect(reverse('otp_validation', kwargs={'email': email}))

            else:
                # Get the error messages from the form and display them
                error_messages = form.errors.values()
                for message in error_messages:
                    messages.error(request, message)
                return render(request, 'accounts/signup.html', {'form': form})

    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)



def otp_validation(request, email):
    if request.user.is_authenticated or 'signup_completed' in request.session:
        return redirect('home')
    
    try:
        otp_instance = UserOTP.objects.get(user__email=email)

        #print(f"Stored OTP: {otp_instance.otp}")

        if request.method == 'POST':
            form = OTPVerificationForm(request.POST)
            if form.is_valid():
                otp_entered = form.cleaned_data['otp']

                #print(f"Entered OTP: {otp_entered}")

                if otp_instance.check_otp(otp_entered):
                    user = otp_instance.user
                    user.is_active = True
                    user.save()
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    otp_instance.delete()
                    messages.success(request, 'OTP verification successful. Your account is now active.')

                    request.session['signup_completed'] = True

                    return redirect('home')
                else:
                    messages.error(request, 'Invalid OTP. Please try again.')
                    
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
                
        else:
            form = OTPVerificationForm()
    except ObjectDoesNotExist:
        messages.error(request, 'Invalid OTP. Please try again or register for a new account.')
        return redirect('otp_validation')

    context = {
        'form': form,
        'email': email,
    }
    return render(request, 'accounts/otp_validation.html', context)


def validate_password(password):
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char in '!@#$%^&*()_\-+=<>?' for char in password):
        return False
    return True


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def logoutpage(request):
    print("Before session clear:", request.session.keys())
    logout(request)
    request.session.clear()
    print("After session clear:", request.session.keys())
    return redirect('loginpage')


# @login_required(login_url='loginpage')
def user_list(request):
    users = Account.objects.all()
    return render(request, 'accounts/user_list.html', {'users': users})


@login_required(login_url='loginpage')
def block_user(request, user_id):
    user = get_object_or_404(Account, id=user_id)

    if user.is_blocked:
        messages.warning(request, 'User is already blocked.')
    else:
        if request.user == user :
            logout(request)
        user.is_blocked = True
        user.is_active = False
        user.save()
        # messages.success(request, 'User has been blocked.')

    return redirect('user_list')


@login_required(login_url='loginpage')
def unblock_user(request, user_id):
    user = get_object_or_404(Account, id=user_id)

    if user.is_active:
        messages.warning(request, 'User is already unblocked.')
    else:
        user.is_active = True
        user.is_blocked = False 
        user.save()
        # messages.success(request, 'User has been unblocked.')

    return redirect('user_list')