from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer 
from products.models import Product
from rest_framework import status
from rest_framework.response import Response


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Nested product details
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity']  # `product_id` for input, `product` for output

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)  # Nested order items
    customer = serializers.ReadOnlyField(source='customer.username')  # Read-only customer name

    class Meta:
        model = Order
        fields = ['id', 'customer', 'created_at', 'items']

    def create(self, validated_data):
        """Create order and its items."""
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        # Create OrderItems linked to the Order
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order

    def update(self, instance, validated_data):
        """Update order and its items."""
        items_data = validated_data.pop('items', None)

        # Update order fields
        instance.save()

        # Update order items
        if items_data:
            instance.items.all().delete()  # Remove old items
            for item_data in items_data:
                OrderItem.objects.create(order=instance, **item_data)

        return instance
        


    def destroy(self, request, *args, **kwargs):
        """Custom delete method to remove an order and its items."""
        instance = self.get_object()
        instance.items.all().delete()  # Delete related OrderItems
        instance.delete()  # Delete the Order itself
        return Response({"message": "Order deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
