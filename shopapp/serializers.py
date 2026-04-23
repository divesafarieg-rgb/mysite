from rest_framework import serializers
from .models import Product, Order

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'discount',
            'created_at', 'archived', 'created_by'
        ]
        read_only_fields = ['id', 'created_at', 'created_by']
        extra_kwargs = {
            'name': {'label': 'Название', 'help_text': 'Название товара'},
            'description': {'label': 'Описание', 'help_text': 'Подробное описание товара'},
            'price': {'label': 'Цена', 'help_text': 'Цена в рублях'},
            'discount': {'label': 'Скидка', 'help_text': 'Скидка в процентах (0-100)'},
            'created_at': {'label': 'Дата создания'},
            'archived': {'label': 'Архивирован', 'help_text': 'True - товар в архиве, False - активный'},
            'created_by': {'label': 'Создал', 'help_text': 'ID пользователя, создавшего товар'},
        }

class OrderSerializer(serializers.ModelSerializer):

    product_ids = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='products',
        many=True,
        write_only=True,
        required=False,
        label="Идентификаторы товаров",
        help_text="Список ID товаров в заказе"
    )
    username = serializers.CharField(
        source='user.username',
        read_only=True,
        label="Имя пользователя",
        help_text="Имя пользователя, создавшего заказ"
    )

    class Meta:
        model = Order
        fields = [
            'id', 'delivery_address', 'promocode', 'created_at',
            'user', 'username', 'products', 'product_ids'
        ]
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'delivery_address': {'label': 'Адрес доставки', 'help_text': 'Полный адрес для доставки'},
            'promocode': {'label': 'Промокод', 'help_text': 'Промокод на скидку'},
            'created_at': {'label': 'Дата создания'},
            'user': {'label': 'Пользователь', 'help_text': 'ID пользователя'},
            'products': {'label': 'Товары', 'help_text': 'Список товаров в заказе'},
        }