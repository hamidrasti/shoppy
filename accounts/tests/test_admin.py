from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

User = get_user_model()


class AdminTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.superadmin_user = User.objects.create_superuser(
            'superadmin',
            email='superadmin@example.com',
            password='pass1234'
        )
        self.client.force_login(self.superadmin_user)
        self.user = User.objects.create_user(
            'user1',
            email='user1@example.com',
            password='pass1234'
        )

    def test_users_listed(self):
        """Test that users are listed on user page"""
        url = reverse('admin:accounts_user_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.user.username)
        self.assertContains(response, self.user.email)

    def test_users_edit_page(self):
        """Test that users edit page works"""
        url = reverse('admin:accounts_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test create user page works"""
        url = reverse('admin:accounts_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
