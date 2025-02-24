import gspread
from google.oauth2.service_account import Credentials
from celery import shared_task
from django.conf import settings
from cleaning.models import Cleaning
from apartment.models import Apartment
from datetime import datetime

@shared_task
def check_google_sheets_for_apartments():
    """Revisa la hoja de cálculo, crea apartamentos nuevos y limpiezas programadas."""
    
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    creds = Credentials.from_service_account_file(settings.GSPREAD_CREDS_FILE, scopes=scopes)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(settings.SHEET_ID).sheet1  
    records = sheet.get_all_records()

    for row in records:
        name = row.get("APARTAMENTO")
        address = row.get("DIRECCIÓN")
        exit_date = row.get("SALIDA")

        if not name or not address or not exit_date:
            continue

        exit_date = datetime.strptime(exit_date, "%d/%m/%Y").date()

        apartment, created = Apartment.objects.get_or_create(
            name=name,
            address=address,
            defaults={"description": "Generado desde Google Sheets", "rooms": 1, "bathrooms": 1, "extra_info": ""}
        )

        if created:
            print(f"🏠 Nuevo apartamento creado: {apartment.name}")

        # Crear una limpieza programada en la fecha de salida si no existe
        if not Cleaning.objects.filter(apartment=apartment, date=exit_date).exists():
            Cleaning.objects.create(apartment=apartment, date=exit_date, status='P')
            print(f"🧹 Limpieza programada para {apartment.name} el {exit_date}")

    return "✔ Google Sheets revisado correctamente"
