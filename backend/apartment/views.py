from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from .models import Apartment, Arrival
from .serializers import ApartmentSerializer, ArrivalSerializer

import gspread
from google.oauth2.service_account import Credentials

from django.conf import settings

from .scripts.check_google_sheets import check_google_sheets

import json

import pandas as pd

# Create your views here.
@api_view(['GET'])
def list_apartments(request):
    apartments = Apartment.objects.all()
    serializer = ApartmentSerializer(apartments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def list_arrivals(request):

    # Filter by apartment name
    apartment_id = request.query_params.get('apartment_id')

    if apartment_id:
        arrivals = Arrival.objects.filter(apartment=apartment_id)
    else:
        arrivals = Arrival.objects.all()

    serializer = ArrivalSerializer(arrivals, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def get_apartments_from_api(request):
    """
    Securely fetches Google Sheets data and triggers check_google_sheets() using a sheet.
    """
    try:
        body = json.loads(request.body)
        special_code = body.get('special_code')
        sheet_name = body.get('sheet_name')  # optional
    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON"}, status=400)

    if special_code != settings.SPECIAL_CODE:
        return Response({"error": "Unauthorized"}, status=403)

    try:
        # Step 1: Connect to Google Sheets
        scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
        creds = Credentials.from_service_account_info(settings.GSPREAD_CREDS, scopes=scopes)
        client = gspread.authorize(creds)

        # Step 2: Open sheet
        sheet = client.open_by_key(settings.SHEET_ID)
        worksheet = sheet.worksheet(sheet_name) if sheet_name else sheet.sheet1

        # Step 3: Convert to DataFrame
        raw_data = worksheet.get_all_values()
        df = pd.DataFrame(raw_data[1:], columns=raw_data[0])

        # Step 4: Run your logic
        data = check_google_sheets(df)

    except Exception as e:
        return Response({"error": str(e)}, status=500)

    return Response({"status": "Task executed successfully!", "data": data})