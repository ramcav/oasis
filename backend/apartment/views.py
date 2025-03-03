from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from .models import Apartment
from .serializers import ApartmentSerializer

import gspread
from google.oauth2.service_account import Credentials

from django.conf import settings

from .scripts import check_google_sheets

import json

# Create your views here.
@api_view(['GET'])
def list_apartments(request):
    apartments = Apartment.objects.all()
    serializer = ApartmentSerializer(apartments, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([])  # No permissions required
@authentication_classes([])  # No authentication required
def get_apartments_from_api(request):
    """
    Securely fetches Google Sheets data and triggers check_google_sheets with special_code.
    """
    # ✅ Extract special_code from request body (more secure than query params)
    try:
        body = json.loads(request.body)
        special_code = body.get('special_code')
    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON"}, status=400)

    # ✅ Validate special_code (Use an environment variable or settings for security)
    if special_code != settings.SPECIAL_CODE:
        return Response({"error": "Unauthorized"}, status=403)

    # ✅ Run Google Sheets processing function with special_code
    data = check_google_sheets.check_google_sheets(special_code)

    return Response({"status": "Task executed successfully!", "data": data})