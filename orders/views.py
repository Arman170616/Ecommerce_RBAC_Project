from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer
from users.permissions import IsCustomer, IsVendor

class OrderViewSet(viewsets.ModelViewSet):
    """
    Customers can place orders, Vendors can only view orders containing their products.
    """
    queryset = Order.objects.all()
    # queryset = Order.objects.prefetch_related('items__product')  # Optimize Many-to-Many
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'customer':
            return Order.objects.filter(customer=user)  # Customers see their own orders
        elif user.role == 'vendor':
            return Order.objects.filter(items__product__vendor=user).distinct()  # Vendors see orders containing their products
        return Order.objects.all()  # Admins see all orders

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
