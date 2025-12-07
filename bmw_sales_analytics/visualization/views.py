from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required


# Home page with Username
def home(request):
    return render(request, 'home.html')

# Signup View
def signup_view(request):
    error = None

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Password validations
        if len(password) < 6:
            error = 'Password must be at least 6 characters long'
        elif not any(char.isdigit() for char in password):
            error = 'Password must contain at least one number'
        elif not any(char.isupper() for char in password):
            error = 'Password must contain at least one uppercase letter'
        elif not any(char in '!@#$%^&*()_+' for char in password):
            error = 'Password must contain at least one special character'
        elif User.objects.filter(username=username).exists():
            error = 'Username already exists'
        elif User.objects.filter(email=email).exists():
            error = 'Email already registered'

        if not error:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return redirect('login')

    return render(request, 'signup.html', {"error": error})


# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid Credentials'})

    return render(request, 'login.html')

# Logout
def logout_view(request):
    logout(request)
    return redirect('login')

# Redirect /visualization → home
def redirect_home(request):
    return redirect('home')

@login_required(login_url='login/')
def models_page(request):
    return render(request, 'models.html', {'razorpay_key_id': settings.RAZORPAY_KEY_ID})


# Payment Gateway Views
# views.py
import csv
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from admin_data.models import CarSale
from django.utils import timezone
import json

@csrf_exempt
def payment_success(request):
    data = json.loads(request.body)
    car = CarSale.objects.filter(model=data['model']).first()
    if car:
        car.purchase_date = timezone.now()
        car.payment_id = data['payment_id']
        car.save()
    CarSale.objects.create(
        model=data['model'],
        year=timezone.now().year,
        region='Asia',
        color='Black',
        fuel_type='Electric',
        transmission='Automatic',
        engine_size_l=2.0,
        mileage_km=15.0,
        price_usd=50000,
        sales_volume=1,
        sales_classification='Retail',
        purchase_date=timezone.now(),
        payment_id=data['payment_id']
    )
    return JsonResponse({'status':'success'})


# views.py
import razorpay
from django.conf import settings
from django.http import JsonResponse

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@csrf_exempt
def create_order(request):
    import razorpay, json
    data = json.loads(request.body)
    amount = int(data['amount']) * 100  # amount in paise
    order_currency = 'INR'
    order = client.order.create(dict(amount=amount, currency=order_currency, payment_capture='1'))
    return JsonResponse(order)
