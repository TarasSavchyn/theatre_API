from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'test@example.com',
            'password': 'test123',
        }
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_obtain_access_token(self):
        url = reverse('user:token_obtain_pair')
        data = {
            'email': self.user_data['email'],
            'password': self.user_data['password'],
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

    def test_refresh_access_token(self):
        url = reverse('user:token_obtain_pair')
        data = {
            'email': self.user_data['email'],
            'password': self.user_data['password'],
        }
        response = self.client.post(url, data)
        refresh_token = response.data['refresh']

        url = reverse('user:token_refresh')
        data = {
            'refresh': refresh_token,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)

    def test_verify_access_token(self):
        url = reverse('user:token_obtain_pair')
        data = {
            'email': self.user_data['email'],
            'password': self.user_data['password'],
        }
        response = self.client.post(url, data)
        access_token = response.data['access']

        url = reverse('user:token_verify')
        data = {
            'token': access_token,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'test@example.com',
            'password': 'test123',
        }

    def test_create_user(self):
        url = reverse('user:create')
        response = self.client.post(url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('email' in response.data)
        self.assertEqual(response.data['email'], self.user_data['email'])

    def test_create_token(self):
        get_user_model().objects.create_user(**self.user_data)
        url = reverse('user:login')
        response = self.client.post(url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

    def test_me(self):
        user = get_user_model().objects.create_user(email='test@example.com', password='test123')
        token = Token.objects.create(user=user)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = self.client.get(reverse('user:manage'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], user.email)

