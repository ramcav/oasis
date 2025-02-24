from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from .models import Apartment
from .serializers import ApartmentSerializer

import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

from django.conf import settings

# Create your views here.
@api_view(['GET'])
def list_apartments(request):
    apartments = Apartment.objects.all()
    serializer = ApartmentSerializer(apartments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def get_apartments_from_api(request):
    
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    creds = Credentials.from_service_account_file(settings.GSPREAD_CREDS_FILE, scopes=scopes)
    
    client = gspread.authorize(creds)
    
    print(settings.SHEET_ID)

    sheet = client.open_by_key(settings.SHEET_ID).sheet1 
    data = sheet.get_all_records()
    
    return Response(data)