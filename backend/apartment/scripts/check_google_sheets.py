import pandas as pd
from django.core.management.base import BaseCommand
from cleaning.models import Cleaning, Review
from apartment.models import Apartment, Arrival
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from notifications.utils import send_notification


def check_google_sheets(df):
    """
    Parse a Google Sheet with apartment bookings and create corresponding objects.
    The sheet has a specific structure where each new header with "fecha de entrada" 
    indicates a new apartment section.
    """
    parsed_data = []
    current_apartment = None
    current_address = None

    # Step 1: Parse the dataframe into a structured format
    for index, row in df.iterrows():
        row_values = row.fillna("").tolist()

        # Detect header row (indicates a new apartment)
        if any("fecha de entrada" in str(cell).lower() for cell in row_values):
            current_apartment = str(row_values[2]).strip()
            current_address = str(row_values[1]).strip()
            continue

        print(row_values)

        # Only process rows that belong to an apartment and have enough data
        if current_apartment and current_address and len(row_values) >= 3:
            guest = str(row_values[0]).strip()
            arrival_raw = str(row_values[3]).strip()
            departure_raw = str(row_values[4]).strip()
            
            # Skip empty rows
            if not arrival_raw or not departure_raw:
                print(f"Skipping row with empty dates: arrival={arrival_raw}, departure={departure_raw}")
                continue

            try:
                # Parse dates
                arrival_date = datetime.strptime(arrival_raw, "%d/%m/%Y").date()
                departure_date = datetime.strptime(departure_raw, "%d/%m/%Y").date()
                
                parsed_data.append({
                    "apartment": current_apartment,
                    "address": current_address,
                    "guest": guest,
                    "arrival_date": arrival_date,
                    "departure_date": departure_date,
                })
            except ValueError:
                # Skip rows with invalid date formats
                print(f"Error parsing dates: arrival={arrival_raw}, departure={departure_raw}")
                continue

    admins = User.objects.filter(profile__role="admin")

    # Step 2: Create or update database objects based on parsed data
    for entry in parsed_data:
        # Create or get apartment
        apartment, apartment_created = Apartment.objects.get_or_create(
            name=entry["apartment"],
            address=entry["address"],
            defaults={
                "description": f"Apartment {entry['apartment']} at {entry['address']}",
                "rooms": 1,
                "bathrooms": 1,
                "extra_info": ""
            }
        )

        if apartment_created:
            print(f"🏠 New apartment created: {apartment.name}")
            send_notification(
                title=f"Nuevo apartamento añadido al sistema",
                message=f"El apartamento {apartment.name} ({apartment.address}) ha sido añadido correctamente.",
                django_user_ids=[admin.id for admin in admins]
            )


        # Create or get arrival
        arrival, arrival_created = Arrival.objects.get_or_create(
            apartment=apartment,
            arrival_date=entry["arrival_date"],
            departure_date=entry["departure_date"]
        )

        if arrival_created:
            # 1. Schedule notification for 3 days before departure time for all users
            three_days_before = entry["departure_date"] - timedelta(days=3)
            send_notification(
                title=f"Salida esperada en {apartment.name} (3 días)",
                message=f"El apartamento {apartment.name} ({apartment.address}) tiene una salida esperada el {entry['departure_date']}.",
                django_user_ids=[user.id for user in User.objects.all()],
                scheduled_time=datetime.combine(three_days_before, datetime.min.time().replace(hour=10))  # 10 AM, 3 days before
            )

            # 2. Schedule notification for 1 day before departure time for all users
            one_day_before = entry["departure_date"] - timedelta(days=1)
            send_notification(
                title=f"Salida esperada mañana en {apartment.name}",
                message=f"El apartamento {apartment.name} ({apartment.address}) tiene una salida esperada mañana {entry['departure_date']}.",
                django_user_ids=[user.id for user in User.objects.all()],
                scheduled_time=datetime.combine(one_day_before, datetime.min.time().replace(hour=10))  # 10 AM, 1 day before
            )
            
            # 3. Schedule notification for departure day for all users
            send_notification(
                title=f"Salida hoy en {apartment.name}",
                message=f"El apartamento {apartment.name} ({apartment.address}) tiene una salida hoy.",
                django_user_ids=[user.id for user in User.objects.all()],
                scheduled_time=datetime.combine(entry["departure_date"], datetime.min.time().replace(hour=8))  # 8 AM on departure day
            )
            
            print(f"📅 New arrival created for {apartment.name} from {entry['arrival_date']} to {entry['departure_date']}")

        # Create cleaning if it doesn't exist
        cleaning, cleaning_created = Cleaning.objects.get_or_create(
            arrival=arrival,
            apartment=apartment,
            defaults={"status": "P"}
        )

        # Create review if it doesn't exist
        if not Review.objects.filter(cleaning=cleaning).exists():
            Review.objects.create(
                cleaning=cleaning,
                date=timezone.now(),
                status='N',
                comment=''
            )

        # Log creations
        if apartment_created:
            print(f"Created new apartment: {apartment.name}")
        if arrival_created:
            print(f"Created new arrival: {apartment.name} from {entry['arrival_date']} to {entry['departure_date']}")
        if cleaning_created:
            print(f"Created new cleaning for {apartment.name} on {entry['departure_date']}")

    # Return statistics
    return {
        "apartments": Apartment.objects.count(),
        "cleanings": Cleaning.objects.count(),
        "reviews": Review.objects.count()
    }
