# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer, CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer

from datetime import datetime

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate refresh and access tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Extract token expiration
            exp_timestamp = refresh.access_token.payload['exp']
            access_expires_at = datetime.utcfromtimestamp(exp_timestamp).isoformat()

            return Response({
                "message": "User created successfully!",
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "access": access_token,
                "refresh": refresh_token,
                "access_expires_at": access_expires_at,
                "role": user.profile.role
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer