from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from products.models import Product

class ProductAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product1 = Product.objects.create(
            name="iPhone 15",
            category="Смартфоны",
            price=85000.00,
            in_stock=True
        )
        self.product2 = Product.objects.create(
            name="Чехол силиконовый",
            category="Аксессуары",
            price=1500.00,
            in_stock=False
        )

    def test_get_products_list(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_categories(self):
        response = self.client.get('/api/products/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Смартфоны", response.data)
        self.assertIn("Аксессуары", response.data)

    def test_get_in_stock(self):
        response = self.client.get('/api/products/in_stock/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "iPhone 15")

    def test_create_product_anonymous_forbidden(self):
        data = {
            "name": "AirPods Pro",
            "category": "Аксессуары",
            "price": 20000.00
        }
        response = self.client.post('/api/products/', data)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

