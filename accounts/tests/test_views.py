from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class ViewsTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_with_valid_username(self):
        """
        Given an active user
        When login via valid username
        Then everything should be ok
        """

        username = 'user1'
        password = 'pass123456'

        User.objects.create_user(
            username,
            password=password
        )

        payload = {'username': username, 'password': password}
        response = self.client.post(reverse('accounts:login'), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertIn('access', response.data)

    def test_login_when_user_is_not_active(self):
        """
        Given a not-active user
        When login
        Then should return unsuccessful response
        """

        username = 'user1'
        password = 'pass123456'

        User.objects.create_user(
            username,
            is_active=False,
            password=password,
        )

        payload = {'username': username, 'password': password}
        response = self.client.post(reverse('accounts:login'), payload)

        self.assertNotIn('user', response.data)
        self.assertNotIn('access', response.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
