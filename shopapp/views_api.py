from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(archived=False)
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'description']
    ordering_fields = ['id', 'name', 'price', 'discount', 'created_at']
    ordering = ['id']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('user').prefetch_related('products')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user', 'promocode', 'created_at']
    ordering_fields = ['id', 'created_at', 'user']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)