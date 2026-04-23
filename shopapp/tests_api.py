from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Product, Order

class ProductAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.product = Product.objects.create(
            name='Тестовый товар',
            price=100.00,
            description='Тестовое описание'
        )

    def test_get_products_list(self):
        response = self.client.get('/shop/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_get_product_detail(self):
        response = self.client.get(f'/shop/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)

    def test_create_product_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'name': 'Новый товар',
            'price': 200.00,
            'description': 'Новое описание'
        }
        response = self.client.post('/shop/api/products/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['created_by'], self.user.id)

    def test_create_product_unauthenticated(self):
        data = {
            'name': 'Новый товар',
            'price': 200.00,
            'description': 'Новое описание'
        }
        response = self.client.post('/shop/api/products/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_product(self):
        self.client.force_authenticate(user=self.user)
        self.product.created_by = self.user
        self.product.save()

        data = {'name': 'Обновлённый товар', 'price': 150.00}
        response = self.client.patch(f'/shop/api/products/{self.product.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Обновлённый товар')

    def test_search_product(self):
        response = self.client.get('/shop/api/products/?search=Тестовый')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_order_product(self):
        response = self.client.get('/shop/api/products/?ordering=-price')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OrderAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.product = Product.objects.create(
            name='Тестовый товар',
            price=100.00
        )
        self.order = Order.objects.create(
            delivery_address='Тестовый адрес',
            promocode='ТЕСТ123',
            user=self.user
        )
        self.order.products.add(self.product)

    def test_get_orders_list_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/shop/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_orders_list_unauthenticated(self):
        response = self.client.get('/shop/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_order_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'delivery_address': 'Новый адрес',
            'promocode': 'НОВЫЙ123',
            'product_ids': [self.product.id]
        }
        response = self.client.post('/shop/api/orders/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], self.user.id)

    def test_filter_orders_by_promocode(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/shop/api/orders/?promocode=ТЕСТ123')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_order_orders_by_created_at(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/shop/api/orders/?ordering=-created_at')
        self.assertEqual(response.status_code, status.HTTP_200_OK)