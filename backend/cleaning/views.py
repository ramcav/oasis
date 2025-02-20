from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Cleaning, Review
from .serializers import CleaningSerializer, ReviewSerializer

# Create your views here.
@api_view(['GET'])
def list_cleanings(request):
    cleanings = Cleaning.objects.all()
    serializer = CleaningSerializer(cleanings, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_cleaning(request):
    serializer = CleaningSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def get_cleaning(request, pk):
    cleaning = Cleaning.objects.get(id=pk)
    serializer = CleaningSerializer(cleaning)
    return Response(serializer.data)

@api_view(['PUT'])
def update_cleaning(request, pk):
    cleaning = Cleaning.objects.get(id=pk)
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
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_review(request, pk):
    review = Review.objects.get(id=pk)
    review.delete()
    return Response(status=204)