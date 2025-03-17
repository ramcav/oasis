import os
import django
from datetime import datetime
from django.utils import timezone
import gspread
from google.oauth2.service_account import Credentials
from cleaning.models import Cleaning, Review
from apartment.models import Apartment, Arrival
from django.contrib.auth.models import User
from datetime import timedelta
from notifications.utils import send_notification


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

def parse_time(time_str):
    if time_str:
        try:
            return datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            print(f"⚠ Invalid time format: {time_str}")
    return None

def check_google_sheets(special_code):
    """Checks Google Sheets, creates new apartments, schedules cleanings, and assigns reviews."""
    from django.conf import settings
    
    if special_code != settings.SPECIAL_CODE:
        print("❌ Invalid special code.")
        return
    
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

    creds = Credentials.from_service_account_info(settings.GSPREAD_CREDS, scopes=scopes)

    client = gspread.authorize(creds)

    sheet = client.open_by_key(settings.SHEET_ID).sheet1  
    records = sheet.get_all_records()

    for row in records:
        name = row.get("APARTAMENTO")
        address = row.get("DIRECCIÓN")
        exit_date = row.get("SALIDA")
        arrival_date = row.get("ENTRADA")
        arrival_time = parse_time(row.get("HORA_LLEGADA"))
        departure_time = parse_time(row.get("HORA_SALIDA"))

        if not name or not address or not exit_date or not arrival_date:
            continue

        exit_date_parsed = datetime.strptime(exit_date, "%d/%m/%Y").date()
        arrival_date_parsed = datetime.strptime(arrival_date, "%d/%m/%Y").date()

        apartment, apartment_created = Apartment.objects.get_or_create(
            name=name,
            address=address,
            defaults={"description": "Generated from Google Sheets", "rooms": 1, "bathrooms": 1, "extra_info": ""}
        )

        if apartment_created:
            admins = User.objects.filter(profile__role='admin')

            print(f"🏠 New apartment created: {apartment.name}")
            send_notification(
                title=f"Nuevo apartamento añadido al sistema",
                message=f"El apartamento {apartment.name} ({apartment.address}) ha sido añadido correctamente.",
                django_user_ids=[admin.id for admin in admins]
            )

        arrival, arrival_created = Arrival.objects.get_or_create(
            apartment=apartment,
            arrival_date=arrival_date_parsed,
            departure_date=exit_date_parsed
        )

        if arrival_created:

            # 1. Schedule notification for 3 days before departure time for all users
            three_days_before = exit_date_parsed - timedelta(days=3)
            send_notification(
                title=f"Salida esperada en {apartment.name} (3 días)",
                message=f"El apartamento {apartment.name} ({apartment.address}) tiene una salida esperada el {exit_date_parsed} a las {departure_time}.",
                django_user_ids=[user.id for user in User.objects.all()],
                scheduled_time=datetime.combine(three_days_before, datetime.min.time().replace(hour=10))  # 10 AM, 3 days before
            )

            # 2. Schedule notification for 1 day before departure time for all users
            one_day_before = exit_date_parsed - timedelta(days=1)
            send_notification(
                title=f"Salida esperada mañana en {apartment.name}",
                message=f"El apartamento {apartment.name} ({apartment.address}) tiene una salida esperada mañana {exit_date_parsed} a las {departure_time}.",
                django_user_ids=[user.id for user in User.objects.all()],
                scheduled_time=datetime.combine(one_day_before, datetime.min.time().replace(hour=10))  # 10 AM, 1 day before
            )
            
            # 3. Schedule notification for departure day for all users
            send_notification(
                title=f"Salida hoy en {apartment.name}",
                message=f"El apartamento {apartment.name} ({apartment.address}) tiene una salida hoy a las {departure_time}.",
                django_user_ids=[user.id for user in User.objects.all()],
                scheduled_time=datetime.combine(exit_date_parsed, datetime.min.time().replace(hour=8))  # 8 AM on departure day
            )
            
            print(f"📅 New arrival created for {apartment.name} from {arrival_date_parsed} to {exit_date_parsed}")

        cleaning, cleaning_created = Cleaning.objects.get_or_create(
            arrival=arrival,
            apartment=apartment,
            defaults={
                'status': 'P',
                'arrival_time': arrival_time,
                'departure_time': departure_time
            }
        )

        if cleaning_created:
            print(f"🧹 Cleaning scheduled for {apartment.name} on {exit_date_parsed}")

        if not Review.objects.filter(cleaning=cleaning).exists():
            Review.objects.create(
                cleaning=cleaning,
                date=timezone.now(),
                status='N',
                comment=''
            )
            print(f"🔍 Review created for cleaning on {exit_date_parsed}")
        
    data = {"apartments": Apartment.objects.count(), "cleanings": Cleaning.objects.count(), "reviews": Review.objects.count()}
        
    return data
