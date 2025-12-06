# visualization/models.py
from django.db import models
from django.utils import timezone

class CarSale(models.Model):
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    region = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    fuel_type = models.CharField(max_length=20)
    transmission = models.CharField(max_length=20)
    engine_size_l = models.FloatField()
    mileage_km = models.IntegerField()
    price_usd = models.FloatField()
    sales_volume = models.IntegerField()
    sales_classification = models.CharField(max_length=20)
    
    # Purchase info
    purchase_date = models.DateTimeField(null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.model} ({self.year})"
