from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from user.tests.datasets.user_datasets import get_user_object

User = get_user_model()


class LoginAPIViewTestCase(APITestCase):

    def setUp(self):
        self.user_data = get_user_object()
        self.user = User.objects.create_user(**self.user_data)
        self.login_url = reverse('login-api')
        self.expected_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        self.expected_ip_address = '127.0.0.1'

    def test_successful_login_with_username(self):
        data = {'username_or_email': self.user.username, 'password': self.user_data.get('password')}
        response = self.client.post(self.login_url, data, **{
            'HTTP_USER_AGENT': self.expected_user_agent,
            'REMOTE_ADDR': self.expected_ip_address,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_successful_login_with_email(self):
        data = {'username_or_email': self.user.email, 'password': self.user_data.get('password')}
        response = self.client.post(self.login_url, data, **{
            'HTTP_USER_AGENT': self.expected_user_agent,
            'REMOTE_ADDR': self.expected_ip_address,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_with_incorrect_password(self):
        data = {'username_or_email': self.user.email, 'password': 'wrongpassword'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('login_error', response.json())

    def test_login_with_nonexistent_username(self):
        data = {'username_or_email': 'nonexistentuser', 'password': 'password123'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username_not_exist', response.json())

    def test_login_with_nonexistent_email(self):
        data = {'username_or_email': 'nonexistentuser@test.com', 'password': 'password123'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email_not_exist', response.json())

    def test_inactive_user_login(self):
        self.user.is_active = False
        self.user.save()
        data = {'username_or_email': self.user.email, 'password': self.user_data.get('password')}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('user_not_verified', response.json())

    def test_login_without_username_or_email(self):
        data = {'password': 'password123'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username_or_email', response.json())

    def test_login_without_password(self):
        data = {'username_or_email': 'testuser'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.json())

    def test_login_with_empty_credentials(self):
        data = {'username_or_email': '', 'password': ''}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username_or_email', response.json())
        self.assertIn('password', response.json())

    def test_login_with_excessive_input_length(self):
        data = {'username_or_email': 'a' * 71, 'password': 'b' * 61}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
