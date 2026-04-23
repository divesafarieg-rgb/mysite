from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    class Meta:
        ordering = ["name", "price"]
        verbose_name = _("product")
        verbose_name_plural = _("products")
        permissions = [
            ("can_create_product", _("Can create product")),
            ("can_edit_product", _("Can edit product")),
        ]

    name = models.CharField(max_length=100, verbose_name=_("name"))
    description = models.TextField(null=False, blank=True, verbose_name=_("description"))
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name=_("price"))
    discount = models.SmallIntegerField(default=0, verbose_name=_("discount"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    archived = models.BooleanField(default=False, verbose_name=_("archived"))
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="products",
        null=True,
        blank=True,
        verbose_name=_("created by")
    )

    def __str__(self):
        return f"Product(pk={self.pk}, name={self.name!r})"

    def get_absolute_url(self):
        return reverse('shopapp:product_details', kwargs={'pk': self.pk})


class Order(models.Model):

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    delivery_address = models.TextField(null=True, blank=True, verbose_name=_("delivery address"))
    promocode = models.CharField(max_length=20, null=False, blank=True, verbose_name=_("promocode"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_("user"))
    products = models.ManyToManyField(Product, related_name="orders", verbose_name=_("products"))

    def __str__(self):
        return f"Order(pk={self.pk}, user={self.user.username!r})"