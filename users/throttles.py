from rest_framework.throttling import UserRateThrottle

class VendorThrottle(UserRateThrottle):
    scope = 'vendor'  # Custom scope for vendor API
