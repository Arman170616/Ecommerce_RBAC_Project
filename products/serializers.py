from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    vendor = serializers.ReadOnlyField(source='vendor.username')  # Show vendor's username

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'vendor']

    def create(self, validated_data):
        validated_data['vendor'] = self.context['request'].user  # Set vendor automatically
        return super().create(validated_data)
