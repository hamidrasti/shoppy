from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from shop.models import Category

User = get_user_model()


def sample_category(**params):
    """Create and return a sample category"""
    defaults = {
        'name': 'Sample category',
    }
    defaults.update(params)

    return Category.objects.create(**defaults)


class CategoriesTestCase(TestCase):

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
        response = self.guest_client.get(reverse('shop:categories-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_list_of_categories(self):
        categories = [sample_category(name='Category1'), sample_category(name='Category2')]

        response = self.client.get(reverse('shop:categories-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(categories), len(response.data))

    def test_retrieve_detail_of_a_category(self):
        category = sample_category()

        response = self.client.get(reverse('shop:categories-detail', args=[category.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], category.id)

    def test_if_given_id_is_invalid_returns_404(self):
        invalid_id = 1

        response = self.client.get(reverse('shop:categories-detail', args=[invalid_id]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_a_category(self):
        payload = {
            'name': 'Category Name',
        }

        response = self.admin_client.post(reverse('shop:categories-list'), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category = Category.objects.get(id=response.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(category, key))

    def test_edit_a_category(self):
        category = sample_category()

        payload = {'name': 'Category Name'}

        self.admin_client.patch(reverse('shop:categories-detail', args=[category.id]), payload)

        category.refresh_from_db()
        self.assertEqual(category.name, payload['name'])

    def test_delete_a_category(self):
        category = sample_category()

        response = self.admin_client.delete(reverse('shop:categories-detail', args=[category.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
