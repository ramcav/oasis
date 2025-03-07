from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile

from datetime import datetime
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import AccessToken

from rest_framework import status
from rest_framework.response import Response

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['role']

class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, write_only=True)
    
    class Meta:
        model = User
        fields = ['id','username', 'password', 'email', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        role = validated_data.pop('role', 'customer')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, role=role)
        return user

    def to_representation(self, instance):
        """Include role in response"""
        representation = super().to_representation(instance)
        representation['role'] = instance.profile.role
        return representation

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        data.update({
            'user_id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'role': self.user.profile.role
        })
        
        access_token = self.get_token(self.user)
        exp_timestamp = access_token.payload['exp']
        data['access_expires_at'] = datetime.utcfromtimestamp(exp_timestamp).isoformat()

        return data

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):

        data = super().validate(attrs)
        

        try:
            # ✅ Use AccessToken class instead of self.token_class
            access_token = AccessToken(data["access"])  
            exp_timestamp = access_token.payload["exp"]
            data["access_expires_at"] = datetime.utcfromtimestamp(exp_timestamp).isoformat()
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        return data
