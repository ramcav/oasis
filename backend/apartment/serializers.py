from rest_framework import serializers
from .models import Apartment, Arrival
from cleaning.models import Cleaning

class CleaningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cleaning
        fields = ['id', 'date', 'status', 'cleaner', 'apartment']

class ArrivalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arrival
        fields = ['id', 'arrival_date', 'departure_date']

class ApartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = ['id', 'name', 'description', 'address']

class ArrivalSerializer(serializers.ModelSerializer):
    apartment = ApartmentListSerializer(read_only=True)
    
    class Meta:
        model = Arrival
        fields = ['id', 'apartment', 'arrival_date', 'departure_date']

class ApartmentSerializer(serializers.ModelSerializer):
    cleanings = CleaningSerializer(many=True, read_only=True)
    arrivals = ArrivalListSerializer(many=True, read_only=True)

    class Meta:
        model = Apartment
        fields = ['id', 'name', 'description', 'address', 'rooms', 'bathrooms', 'extra_info', 'date_created', 'cleanings', 'arrivals']
