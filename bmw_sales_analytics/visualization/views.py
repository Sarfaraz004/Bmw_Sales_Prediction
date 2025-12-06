from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required


# Home page with Username
def home(request):
    return render(request, 'home.html')

# Signup View
def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('login')

    return render(request, 'signup.html')

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
