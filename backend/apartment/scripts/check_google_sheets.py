import os
import django
from datetime import datetime
from django.utils import timezone
import gspread
from google.oauth2.service_account import Credentials
from cleaning.models import Cleaning, Review
from apartment.models import Apartment

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

            # ✅ Check if a review already exists before creating one
            if not Review.objects.filter(cleaning=cleaning).exists():
                Review.objects.create(
                    cleaning=cleaning,
                    date=timezone.now(),
                    status='N',
                    comment=''
                )
                print(f"🔍 Review created for cleaning on {exit_date}")


    print("✔ Google Sheets successfully checked and updated.")

if __name__ == "__main__":
    check_google_sheets()
