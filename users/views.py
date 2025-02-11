from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
