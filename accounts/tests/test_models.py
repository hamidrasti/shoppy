from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class ModelsTestCase(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'user@example.com'
        password = 'pass1234'
        user = User.objects.create_user(
            'user1',
            email=email,
            password='pass1234'
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_email_is_normalized(self):
        """Test if email is normalized"""
        email = 'user@EXAMPLE.com'
        user = User.objects.create_user(
            'user1',
            email=email,
            password='pass1234',
        )

        self.assertEqual(user.email, email.lower())

    def test_email_is_invalid(self):
        """Test if an invalid email raises error"""
        with self.assertRaises(ValueError):
            User.objects.create_user(None, 'pass1234')

    def test_create_super_user(self):
        """Test creating a new superuser"""
        user = User.objects.create_superuser(
            'admin@example.com',
            'pass1234'
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
