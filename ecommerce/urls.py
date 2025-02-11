from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import VendorViewSet
from products.views import ProductViewSet
from orders.views import OrderViewSet
from django.contrib import admin

router = DefaultRouter()
router.register(r'vendors', VendorViewSet, basename='vendor')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/users/', include('users.urls')),
]
