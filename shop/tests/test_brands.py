from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from shop.models import Brand

User = get_user_model()


def sample_brand(**params):
    """Create and return a sample brand"""
    defaults = {
        'name': 'Sample brand',
    }
    defaults.update(params)

    return Brand.objects.create(**defaults)


class BrandsTestCase(TestCase):

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

    def test_if_user_is_anonymous_returns_401(self):
        response = self.guest_client.get(reverse('shop:brands-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_list_of_brands(self):
        brands = [sample_brand(name='Brand1'), sample_brand(name='Brand2')]

        response = self.client.get(reverse('shop:brands-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(brands), len(response.data))

    def test_retrieve_detail_of_a_brand(self):
        brand = sample_brand()

        response = self.client.get(reverse('shop:brands-detail', args=[brand.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], brand.id)

    def test_if_given_id_is_invalid_returns_404(self):
        invalid_id = 1

        response = self.client.get(reverse('shop:brands-detail', args=[invalid_id]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_a_brand(self):
        payload = {
            'name': 'Brand Name',
        }

        response = self.admin_client.post(reverse('shop:brands-list'), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        brand = Brand.objects.get(id=response.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(brand, key))

    def test_edit_a_brand(self):
        brand = sample_brand()

        payload = {'name': 'Brand Name'}

        self.admin_client.patch(reverse('shop:brands-detail', args=[brand.id]), payload)

        brand.refresh_from_db()
        self.assertEqual(brand.name, payload['name'])

    def test_delete_a_brand(self):
        brand = sample_brand()

        response = self.admin_client.delete(reverse('shop:brands-detail', args=[brand.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
