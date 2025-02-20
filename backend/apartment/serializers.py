from rest_framework import serializers
from .models import Apartment
from cleaning.models import Cleaning

class CleaningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cleaning
        fields = ['id', 'date', 'status', 'cleaner', 'apartment']

class ApartmentSerializer(serializers.ModelSerializer):
    cleanings = CleaningSerializer(many=True, read_only=True)

    class Meta:
        model = Apartment
        fields = ['id', 'name', 'description', 'address', 'rooms', 'bathrooms', 'extra_info', 'date_created', 'cleanings']