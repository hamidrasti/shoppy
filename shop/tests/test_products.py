from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from djmoney.money import Money
from rest_framework import status
from rest_framework.test import APIClient

from shop.models import Product, Brand, Category

User = get_user_model()


def sample_brand(name='Sample brand'):
    return Brand.objects.create(name=name)


def sample_category(name='Sample category'):
    return Category.objects.create(name=name)


def sample_product(**params):
    """Create and return a sample product"""
    defaults = {
        'title': 'Sample product',
        'description': '',
        'price': Money(1, 'USD'),
        'brand': sample_brand(),
        'category': sample_category(),
    }
    defaults.update(params)
    return Product.objects.create(**defaults)


class ProductsTestCase(TestCase):

    def setUp(self):
        self.guest_client = APIClient()

        self.client = APIClient()
        self.user = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='pass123456',
        )
        self.client.force_authenticate(self.user)

        self.admin_client = APIClient()
        self.superadmin_user = User.objects.create_superuser(
            'superadmin',
            email='superadmin@example.com',
            password='pass1234'
        )
        self.admin_client.force_authenticate(self.superadmin_user)

    def test_retrieve_list_of_products(self):
        products = [sample_product(title='Product1'), sample_product(title='Product2')]

        response = self.client.get(reverse('shop:products-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], len(products))

    def test_retrieve_detail_of_a_product(self):
        product = sample_product()

        response = self.client.get(reverse('shop:products-detail', args=[product.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], product.id)

    def test_if_given_id_is_invalid_returns_404(self):
        invalid_id = 1

        response = self.client.get(reverse('shop:products-detail', args=[invalid_id]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_a_product(self):
        payload = {
            'title': 'Product Name',
            'description': 'Some description',
            'price': 100000,
            'brand_id': sample_brand().id,
            'category_id': sample_category().id,
        }

        response = self.admin_client.post(reverse('shop:products-list'), payload)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product = Product.objects.get(id=response.data['id'])

        self.assertEqual(payload['title'], getattr(product, 'title'))
        self.assertEqual(payload['description'], getattr(product, 'description'))
        self.assertEqual(payload['price'], getattr(product, 'price').amount)
        self.assertEqual(payload['brand_id'], getattr(product, 'brand_id'))
        self.assertEqual(payload['category_id'], getattr(product, 'category_id'))

    def test_edit_a_product(self):
        product = sample_product()

        payload = {
            'title': 'Edited Product Name',
            'price': 100,
        }

        self.admin_client.patch(reverse('shop:products-detail', args=[product.id]), payload)

        product.refresh_from_db()

        self.assertEqual(product.title, payload['title'])
        self.assertEqual(product.price.amount, payload['price'])

    def test_if_only_admins_can_edit_a_product(self):
        product = sample_product()

        payload = {'title': 'Edited Product Name'}

        response = self.client.patch(reverse('shop:products-detail', args=[product.id]), payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_a_product_returns_204(self):
        product = sample_product()

        response = self.admin_client.delete(reverse('shop:products-detail', args=[product.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_if_user_is_not_admin_for_deleting_a_product_returns_403(self):
        product = sample_product()

        response = self.client.delete(reverse('shop:products-detail', args=[product.id]))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
