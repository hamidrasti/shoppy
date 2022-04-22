from uuid import UUID

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from shop.models import Cart

User = get_user_model()


def sample_cart():
    return Cart.objects.create()


class CartsTestCase(TestCase):

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
        response = self.guest_client.get(reverse('shop:carts-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_detail_of_a_cart(self):
        cart = sample_cart()

        response = self.client.get(reverse('shop:carts-detail', args=[cart.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UUID(response.data['id']), cart.id)

    def test_if_given_id_is_invalid_returns_404(self):
        invalid_id = 'wrong_id'

        response = self.client.get(reverse('shop:carts-detail', args=[invalid_id]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_a_cart(self):
        payload = {}

        response = self.admin_client.post(reverse('shop:carts-list'), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)

    def test_delete_a_cart(self):
        cart = sample_cart()

        response = self.admin_client.delete(reverse('shop:carts-detail', args=[cart.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_retrieve_list_of_cartitems(self):
        cart = sample_cart()

        response = self.client.get(reverse('shop:cartitems-list', args=[cart.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(brands), len(response.data))

    def test_create_an_order_with_empty_cart_returns_400(self):
        payload = {
            'cart_id': str(sample_cart().id)
        }

        response = self.admin_client.post(reverse('shop:orders-list'), payload)
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
