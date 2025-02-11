from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsAdmin(BasePermission):
    """
    Custom permission to allow only admins to access this view.
    """

    def has_permission(self, request, view):
        # Ensure user is authenticated and has role 'admin'
        return request.user.is_authenticated and request.user.role == 'admin'


class IsVendor(permissions.BasePermission):
    """
    Allows access only to Vendor users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'vendor'

class IsCustomer(permissions.BasePermission):
    """
    Allows access only to Customer users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'customer'

class IsVendorOrAdmin(permissions.BasePermission):
    """
    Allows access to Vendors for their own objects and Admins for all objects.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role in ['admin', 'vendor'])

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin' or obj.user == request.user
