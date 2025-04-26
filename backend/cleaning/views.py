from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from .models import Cleaning, Review
from .serializers import CleaningSerializer, ReviewSerializer

from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from datetime import datetime

from notifications.utils import send_notification
from django.contrib.auth.models import User
@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([JWTAuthentication])
def list_cleanings(request):
    user_id = request.query_params.get('cleaner_id', None)
    start_date = request.query_params.get('start_date', None)
    
    cleanings = Cleaning.objects.all()
    
    if user_id not in ['', None]:
        cleanings = cleanings.filter(cleaner=user_id)
    
    if start_date:
        if start_date == 'null':
            start_date = datetime.now().strftime('%Y-%m-%d')
        cleanings = cleanings.filter(arrival__departure_date__gte=start_date)
    
    cleanings = cleanings.order_by('arrival__departure_date')
    
    serializer = CleaningSerializer(cleanings, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def get_cleaning(request, pk):
    cleaning = Cleaning.objects.get(id=pk)
    serializer = CleaningSerializer(cleaning)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([JWTAuthentication])
def list_cleanings_grouped_by_date(request):
    cleanings = Cleaning.objects.all()
    grouped_cleanings = {}
    for cleaning in cleanings:
        date = cleaning.arrival.departure_date.strftime('%Y-%m-%d')
        if date not in grouped_cleanings:
            grouped_cleanings[date] = []
        grouped_cleanings[date].append(CleaningSerializer(cleaning).data)
    
    result = [{'date': date, 'cleanings': cleanings} for date, cleanings in grouped_cleanings.items()]
    return Response(result)

@api_view(['POST'])
def create_cleaning(request):
    serializer = CleaningSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
@permission_classes([])
@authentication_classes([JWTAuthentication])
def update_cleaning(request, pk):
    cleaning = Cleaning.objects.get(id=pk)
    
    if 'cleaner' in request.data:
        request.data['cleaner'] = int(request.data['cleaner'])
        print(request.data['cleaner'])
    serializer = CleaningSerializer(instance=cleaning, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def list_reviews(request):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_review(request, pk):
    review = Review.objects.get(id=pk)
    serializer = ReviewSerializer(review)
    return Response(serializer.data)

@api_view(['POST'])
def create_review(request):
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def update_review(request, pk):
    review = Review.objects.get(id=pk)
    serializer = ReviewSerializer(instance=review, data=request.data)
    admins = User.objects.filter(profile__role="admin")
    print(request.data['handyman'])
    if serializer.is_valid():
        serializer.save()
        print(serializer.data['handyman'])
        if serializer.data['status'] == 'C':
            send_notification(
                title=f"Revisión en {review.arrival.apartment.name}",
                message=f"Revisión para {review.arrival.apartment.name} el {review.arrival.departure_date} ha sido actualizada.",
                django_user_ids=[user.id for user in admins]
            )
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_review(request, pk):
    review = Review.objects.get(id=pk)
    review.delete()
    return Response(status=204)