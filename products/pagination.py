from rest_framework.pagination import PageNumberPagination

class ProductPagination(PageNumberPagination):
    page_size = 5  # Each page will have 5 products
    page_size_query_param = 'page_size'  # Allows users to customize page size
    max_page_size = 100  # Maximum allowed page size
