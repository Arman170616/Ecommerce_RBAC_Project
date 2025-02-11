from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import ProductSerializer
from users.permissions import IsVendor, IsAdmin, IsVendorOrAdmin
from rest_framework.throttling import ScopedRateThrottle
from .pagination import ProductPagination

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets, permissions



''' FOR REDIS Use this code '''

# from django.core.cache import cache
# from rest_framework.response import Response
# from rest_framework.decorators import action

# class ProductViewSet(viewsets.ModelViewSet):
#     @action(detail=False, methods=['get'])
#     def cached_products(self, request):
#         """
#         Returns cached product list.
#         """
#         cache_key = "cached_product_list"
#         products = cache.get(cache_key)

#         if not products:
#             products = Product.objects.all()
#             cache.set(cache_key, products, timeout=60*5)  # Cache for 5 minutes

#         serializer = self.get_serializer(products, many=True)
#         return Response(serializer.data)



class IsVendorOrAdmin(permissions.BasePermission):
    """
    Vendors can manage their own products, Admins can manage all.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin' or obj.vendor == request.user  # Only vendor or admin

class ProductViewSet(viewsets.ModelViewSet):
    """
    Vendors can manage their own products, Admins can manage all.
    """
    queryset = Product.objects.all()
    # queryset = Product.objects.select_related('vendor')  # Optimized query
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsVendorOrAdmin]

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'vendor'

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['vendor', 'price']  # Exact filtering
    search_fields = ['name', 'description']  # Full-text search
    ordering_fields = ['price', 'name']  # Sorting options
    pagination_class = ProductPagination 

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Product.objects.all()  # Admin sees all
        return Product.objects.filter(vendor=user)  # Vendor sees only their own

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user)