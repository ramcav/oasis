from rest_framework import serializers
from .models import Cleaning, Review

from apartment.serializers import ApartmentSerializer

from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ReviewSerializer(serializers.ModelSerializer):
    handyman = UserSerializer(read_only=True)
    handyman_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='handyman', allow_null=True
    )
    class Meta:
        model = Review
        fields = ['id', 'handyman','handyman_id', 'date', 'status', 'comment']
        read_only_fields = ['id', 'date']

class CleaningSerializer(serializers.ModelSerializer):
    cleaner = UserSerializer(read_only=True)
    cleaner_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='cleaner', allow_null=True
    )
    apartment = ApartmentSerializer(read_only=True)
    review  = ReviewSerializer(read_only=True)
    date = serializers.SerializerMethodField()
    
    class Meta:
        model = Cleaning
        fields = [
            'id', 'date', 'status', 'cleaner', 'cleaner_id', 
            'apartment', 'review', 'arrival_time', 'departure_time'
        ]
        read_only_fields = ['id', 'date']

    def get_date(self, obj):
        return obj.arrival.departure_date if obj.arrival else None