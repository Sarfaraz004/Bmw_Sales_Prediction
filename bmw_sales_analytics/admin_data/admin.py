# visualization/admin.py
from django.contrib import admin
from .models import CarSale

@admin.register(CarSale)
class CarSaleAdmin(admin.ModelAdmin):
    list_display = ("model", "year", "region", "color", "price_usd", "sales_volume", "purchase_date")
    search_fields = ("model", "region", "color")
    list_filter = ("year", "region", "fuel_type", "transmission", "sales_classification")
