from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.core.cache import cache

from .models import Product, Order
from .serializers import OrderSerializer

class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {}
        return render(request, 'shopapp/shop-index.html', context=context)

class ProductDetailsView(DetailView):
    template_name = "shopapp/products-details.html"
    model = Product
    context_object_name = "product"

class ProductsListView(ListView):
    template_name = "shopapp/products-list.html"
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)

class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    fields = "name", "price", "description", "discount"
    success_url = reverse_lazy("shopapp:products_list")
    permission_required = "shopapp.can_create_product"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = "name", "price", "description", "discount"
    template_name_suffix = "_update_form"

    def test_func(self):
        product = self.get_object()
        user = self.request.user

        if user.is_superuser:
            return True

        return (user.has_perm("shopapp.can_edit_product") and
                product.created_by == user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("You don't have permission to edit this product")
        return super().handle_no_permission()

    def get_success_url(self):
        return reverse_lazy(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)

class OrdersListView(ListView):
    template_name = "shopapp/order_list.html"
    context_object_name = "object_list"
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )

class OrderDetailView(DetailView):
    template_name = "shopapp/order_detail.html"
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


class UserOrdersListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'shopapp/user_orders_list.html'
    context_object_name = 'orders'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        self.owner = get_object_or_404(User, pk=self.kwargs['user_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Order.objects.filter(
            user=self.owner
        ).select_related('user').prefetch_related('products').order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = self.owner
        return context


class UserOrdersExportView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user_id = kwargs['user_id']

        user = get_object_or_404(User, pk=user_id)

        cache_key = f'user_orders_export_{user_id}'

        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return JsonResponse({
                'status': 'cached',
                'user_id': user_id,
                'username': user.username,
                'orders': cached_data
            }, json_dumps_params={'ensure_ascii': False, 'indent': 2})

        orders = Order.objects.filter(
            user=user
        ).select_related('user').prefetch_related('products').order_by('id')

        serializer = OrderSerializer(orders, many=True)
        orders_data = serializer.data

        cache.set(cache_key, orders_data, timeout=300)

        return JsonResponse({
            'status': 'fresh',
            'user_id': user_id,
            'username': user.username,
            'orders': orders_data
        }, json_dumps_params={'ensure_ascii': False, 'indent': 2})
@method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
class OrdersExportView(View):

    def get(self, request):
        orders = Order.objects.select_related('user').prefetch_related('products').all()

        orders_data = []
        for order in orders:
            orders_data.append({
                'id': order.pk,
                'delivery_address': order.delivery_address,
                'promocode': order.promocode,
                'user_id': order.user.id,
                'product_ids': [product.pk for product in order.products.all()],
                'created_at': order.created_at.isoformat() if order.created_at else None,
            })

        return JsonResponse({'orders': orders_data}, json_dumps_params={'ensure_ascii': False, 'indent': 2})