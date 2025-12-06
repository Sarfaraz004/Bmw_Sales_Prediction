# visualization/views.py
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import CarSale

def dashboard(request):
    cars_list = CarSale.objects.all().order_by('-year')
    paginator = Paginator(cars_list, 25)  # 25 rows per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_dashboard.html', {'page_obj': page_obj})

# visualization/views.py
from django.shortcuts import render
from .models import CarSale
from django.http import JsonResponse
import pandas as pd

def analytics_dashboard(request):
    models = CarSale.objects.values_list('model', flat=True).distinct()
    return render(request, "analytics.html", {"models": models})


def fetch_model_data(request, model):
    cars = CarSale.objects.filter(model=model).order_by("year")
    df = pd.DataFrame(list(cars.values()))

    response = {
        "years": df["year"].tolist(),
        "prices": df["price_usd"].tolist(),
        "sales": df["sales_volume"].tolist(),
        "region_data": df.groupby("region")["sales_volume"].sum().to_dict()
    }

    return JsonResponse(response)

