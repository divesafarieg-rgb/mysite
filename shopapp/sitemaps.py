from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product


class ShopSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Product.objects.filter(archived=False)

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return obj.get_absolute_url()


class StaticViewSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return ['shopapp:index', 'shopapp:products_list', 'shopapp:orders_list']

    def location(self, item):
        return reverse(item)