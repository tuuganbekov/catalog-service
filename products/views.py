from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Product
from .serializers import ProductSerializer


class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = (
        Product.objects
        .select_related("category")
        .prefetch_related("images")
        .filter(is_active=True)
    )
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ("name", "description", )
    filterset_fields = (
        "category",
        "stock_quantity",
    )
    ordering_fields = ("created_at", "price", "stock_quantity", )
