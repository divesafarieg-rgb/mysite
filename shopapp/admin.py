from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import path
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
import csv
import io

from .models import Product, Order
from .admin_mixins import ExportAsCSVMixin
from .forms import OrderImportForm


class OrderInline(admin.TabularInline):
    model = Product.orders.through


@admin.action(description="Archive products")
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description="Unarchive products")
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        mark_archived,
        mark_unarchived,
        "export_csv",
    ]
    inlines = [
        OrderInline,
    ]
    list_display = "pk", "name", "description_short", "price", "discount", "archived", "created_by"
    list_display_links = "pk", "name"
    ordering = "-name", "pk"
    search_fields = "name", "description"
    fieldsets = [
        (None, {
            "fields": ("name", "description"),
        }),
        ("Price options", {
            "fields": ("price", "discount"),
            "classes": ("wide", "collapse"),
        }),
        ("Author", {
            "fields": ("created_by",),
            "classes": ("collapse",),
        }),
        ("Extra options", {
            "fields": ("archived",),
            "classes": ("collapse",),
            "description": "Extra options. Field 'archived' is for soft delete",
        })
    ]

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + "..."


class ProductInline(admin.TabularInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    change_list_template = "admin/shopapp/order/change_list.html"
    inlines = [
        ProductInline,
    ]
    list_display = "id", "delivery_address", "promocode", "created_at", "user_verbose"
    list_filter = ("promocode", "created_at", "user")
    search_fields = ("delivery_address", "promocode", "user__username")

    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("products")

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username

    user_verbose.short_description = _("User")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import/', self.import_orders, name='import_orders'),
        ]
        return custom_urls + urls

    def import_orders(self, request):
        if request.method == 'POST':
            form = OrderImportForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES['csv_file']

                data_set = csv_file.read().decode('utf-8')
                io_string = io.StringIO(data_set)
                reader = csv.DictReader(io_string)

                imported_count = 0
                errors = []

                for row in reader:
                    try:
                        product_ids = [int(id.strip()) for id in row['product_ids'].split(',')]
                        products = Product.objects.filter(id__in=product_ids)

                        if len(products) != len(product_ids):
                            errors.append(f"Товары не найдены для ID: {product_ids}")
                            continue

                        order = Order.objects.create(
                            delivery_address=row['delivery_address'],
                            promocode=row['promocode'],
                            user_id=row['user_id']
                        )
                        order.products.set(products)
                        imported_count += 1

                    except Exception as e:
                        errors.append(f"Ошибка в строке: {row}, ошибка: {str(e)}")

                if imported_count > 0:
                    messages.success(request, f"Успешно импортировано {imported_count} заказов")
                if errors:
                    for error in errors[:5]:
                        messages.error(request, error)

                return HttpResponseRedirect('../')
        else:
            form = OrderImportForm()

        context = {
            'form': form,
            'title': 'Импорт заказов из CSV',
        }
        return render(request, 'admin/csv_form.html', context)