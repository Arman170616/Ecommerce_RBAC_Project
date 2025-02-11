from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Vendor



User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    


class VendorSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")  # Show username

    class Meta:
        model = Vendor
        fields = ["id", "user", "store_name", "created_at"]

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["user"] = request.user  # Assign the vendor to the logged-in user
        return super().create(validated_data)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token
