# visualization/utils.py
import pandas as pd
from .models import CarSale
from django.db import transaction

def import_csv(file_path):
    """
    Import car sales data from a CSV file into the database.
    Deletes previous records and imports all rows from CSV.
    """
    df = pd.read_csv(file_path)

    # Delete previous data
    CarSale.objects.all().delete()

    records_to_create = [
        CarSale(
            model=row['Model'],
            year=row['Year'],
            region=row['Region'],
            color=row['Color'],
            fuel_type=row['Fuel_Type'],
            transmission=row['Transmission'],
            engine_size_l=row['Engine_Size_L'],
            mileage_km=row['Mileage_KM'],
            price_usd=row['Price_USD'],
            sales_volume=row['Sales_Volume'],
            sales_classification=row['Sales_Classification']
        )
        for _, row in df.iterrows()
    ]

    with transaction.atomic():
        CarSale.objects.bulk_create(records_to_create, batch_size=1000)

    print(f"Imported {len(df)} rows from {file_path} successfully.")
