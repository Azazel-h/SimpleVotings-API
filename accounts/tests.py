from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework.authtoken.models import Token

class UserTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.data = {
            'username': 'test_username',
            'password': 'test_pass',
            'password2': 'test_pass',
        }

    def test_sign_up(self):
        response = self.client.post(reverse('signup'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        new_user = User.objects.get(id=1)
        self.assertEqual(new_user.username, self.data['username'])

    def test_existed_username(self):
        response = self.client.post(reverse('signup'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(reverse('signup'), self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login(self):
        User.objects.create_user(username=self.data['username'], password=self.data['password'])
        response = self.client.post(reverse('login'), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

    def test_logout(self):
        User.objects.create_user(username=self.data['username'], password=self.data['password'])
        response = self.client.post(reverse('login'), self.data)
        token = response.data['token']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile(self):
        User.objects.create_user(username=self.data['username'], password=self.data['password'])
        response = self.client.post(reverse('login'), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)