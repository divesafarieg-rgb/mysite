from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed
from .models import Product


class LatestProductsFeed(Feed):
    title = "Последние товары в магазине"
    link = "/shop/"
    description = "Обновления каталога товаров нашего магазина"
    feed_type = Rss201rev2Feed

    def items(self):
        return Product.objects.filter(archived=False).order_by('-created_at')[:10]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description or "Описание отсутствует"

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.created_at

    def item_author_name(self, item):
        return item.created_by.username if item.created_by else "Администратор"