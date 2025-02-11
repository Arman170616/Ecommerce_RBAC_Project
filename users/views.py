from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from django.contrib.auth import get_user_model

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor
from .serializers import VendorSerializer



User = get_user_model()

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer, VendorSerializer
from .permissions import IsAdmin

class IsAdminOrSelf(permissions.BasePermission):
    """
    Admins can access all vendors, and vendors can manage only their profile.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.role == "admin" or obj.user == request.user

class VendorViewSet(viewsets.ModelViewSet):
    """
    Admins can manage all vendors, while vendors can manage only their own profile.
    """
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSelf]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Vendor.objects.all()  # Admin sees all vendors
        return Vendor.objects.filter(user=user)  # Vendors see only their own profile

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Assign logged-in user as vendor