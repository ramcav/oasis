import gspread
from google.oauth2.service_account import Credentials
from celery import shared_task
from django.conf import settings
from cleaning.models import Cleaning, Review
from apartment.models import Apartment
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

def parse_time(time_str):
    """Helper function to parse time in HH:MM format, return None if empty."""
    if time_str:
        try:
            return datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            print(f"⚠ Invalid time format: {time_str}")
    return None

@shared_task
def check_google_sheets_for_apartments():
    """Checks the Google Sheet, creates new apartments, schedules cleanings, and assigns reviews."""
    
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    creds = Credentials.from_service_account_file(settings.GSPREAD_CREDS_FILE, scopes=scopes)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(settings.SHEET_ID).sheet1  
    records = sheet.get_all_records()

    for row in records:
        name = row.get("APARTAMENTO")
        address = row.get("DIRECCIÓN")
        exit_date = row.get("SALIDA")
        arrival_time = parse_time(row.get("HORA_LLEGADA"))
        departure_time = parse_time(row.get("HORA_SALIDA"))

        if not name or not address or not exit_date:
            continue

        exit_date = datetime.strptime(exit_date, "%d/%m/%Y").date()

        apartment, created = Apartment.objects.get_or_create(
            name=name,
            address=address,
            defaults={"description": "Generated from Google Sheets", "rooms": 1, "bathrooms": 1, "extra_info": ""}
        )

        if created:
            print(f"🏠 New apartment created: {apartment.name}")

        # Schedule a cleaning if one does not already exist for this apartment on the exit date
        if not Cleaning.objects.filter(apartment=apartment, date=exit_date).exists():
            cleaning = Cleaning.objects.create(
                apartment=apartment, 
                date=exit_date, 
                status='P', 
                arrival_time=arrival_time, 
                departure_time=departure_time
            )
            print(f"🧹 Cleaning scheduled for {apartment.name} on {exit_date}")
            
            # Automatically create a review for this cleaning
            Review.objects.create(
                cleaning=cleaning,
                date=timezone.now(),
                status='N',
                comment=''
            )
            print(f"🔍 Review created for cleaning on {exit_date}")

    return "✔ Google Sheets successfully checked and updated."
