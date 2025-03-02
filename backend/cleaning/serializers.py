from rest_framework import serializers
from .models import Cleaning, Review

from apartment.serializers import ApartmentSerializer

from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ReviewSerializer(serializers.ModelSerializer):
    handyman = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = Review
        fields = ['id', 'handyman','date', 'status', 'comment']
        read_only_fields = ['id', 'date']

class CleaningSerializer(serializers.ModelSerializer):
    cleaner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    apartment = ApartmentSerializer(read_only=True)
    review  = ReviewSerializer(read_only=True)
    
    class Meta:
        model = Cleaning
        fields = ['id', 'date', 'status', 'cleaner', 'apartment', 'review', 'arrival_time', 'departure_time']
        read_only_fields = ['id', 'date']