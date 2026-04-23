from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ShopIndexView,
    ProductDetailsView,
    ProductsListView,
    OrdersListView,
    OrderDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    OrdersExportView,
    UserOrdersListView,
    UserOrdersExportView,
)
from .views_api import ProductViewSet, OrderViewSet
from .feeds import LatestProductsFeed

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='api-product')
router.register(r'orders', OrderViewSet, basename='api-order')

app_name = "shopapp"

urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/archive/", ProductDeleteView.as_view(), name="product_delete"),
    path("orders/", OrdersListView.as_view(), name="orders_list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_details"),
    path("orders/export/", OrdersExportView.as_view(), name="orders_export"),

    path("users/<int:user_id>/orders/", UserOrdersListView.as_view(), name="user_orders"),
    path("users/<int:user_id>/orders/export/", UserOrdersExportView.as_view(), name="user_orders_export"),

    path("products/latest/feed/", LatestProductsFeed(), name="products_feed"),

    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]