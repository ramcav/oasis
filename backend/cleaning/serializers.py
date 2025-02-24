from rest_framework import serializers
from .models import Cleaning, Review

from apartment.serializers import ApartmentSerializer

from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CleaningSerializer(serializers.ModelSerializer):
    cleaner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    apartment = ApartmentSerializer(read_only=True)
    
    class Meta:
        model = Cleaning
        fields = ['id', 'date', 'status', 'cleaner', 'apartment']
        read_only_fields = ['id', 'date']
        
class ReviewSerializer(serializers.ModelSerializer):
    handyman = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    cleaning = CleaningSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'handyman', 'cleaning', 'date', 'status', 'comment']
        read_only_fields = ['id', 'date']