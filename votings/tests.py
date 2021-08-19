from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class VotingsViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.client_data = {
            'username': 'test_username',
            'password': 'test_pass',
            'password2': 'test_pass',
        }
        self.voting_data = {
            'title': 'test_voting',
            'type': 0,
        }
        user = User.objects.create_user(username=self.client_data['username'], password=self.client_data['password'])
        user.save()

    def test_votings_list(self):
        # Checking an unauthorized user
        response = self.client.get(reverse('list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Checking an authorized user
        response = self.client.post(reverse('login'), self.client_data)
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(reverse('list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create_voting(self):
        # Checking an unauthorized user
        response = self.client.post(reverse('list'), self.voting_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Checking an authorized user
        self.client.login(username=self.client_data['username'],
                          password=self.client_data['password'])
        response = self.client.post(reverse('login'), self.client_data)
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        # Creating 4 new votings
        for i in range(4):
            response = self.client.post(reverse('list'), self.voting_data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(reverse('list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_get_voting_details(self):
        response = self.client.post(reverse('login'), self.client_data)
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        # Creating a new voting
        response = self.client.post(reverse('list'), self.voting_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Checking its details
        response = self.client.get(reverse('details', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)
        # Checking an unauthorized user
        self.client.credentials()
        response = self.client.get(reverse('details', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_creating_choice(self):
        response = self.client.post(reverse('login'), self.client_data)
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post(reverse('list'), self.voting_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Creating a new choice
        response = self.client.put(reverse('details', kwargs={'pk': 1}), {'text' : 'test_text'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Checking if it was created
        response = self.client.get(reverse('details', kwargs={'pk': 1}))
        self.assertEqual(len(response.data['choices']), 1)
        # Checking its text
        self.assertEqual(response.data['choices'][0]['text'], 'test_text')
        # Creating the second one
        response = self.client.put(reverse('details', kwargs={'pk': 1}), {'text': 'test_text'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(reverse('details', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['choices']), 2)
        self.assertEqual(response.data['choices'][1]['text'], 'test_text')
        # Checking an unauthorized user
        self.client.credentials()
        response = self.client.put(reverse('details', kwargs={'pk': 1}), {'text' : 'test_text'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_voting_type_0(self):
        self.client.login(username=self.client_data['username'],
                          password=self.client_data['password'])
        response = self.client.post(reverse('login'), self.client_data)
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        # Creating a new voting
        response = self.client.post(reverse('list'), self.voting_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Creating a new choices
        response = self.client.put(reverse('details', kwargs={'pk': 1}), {'text': 'test_text'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.put(reverse('details', kwargs={'pk': 1}), {'text': 'test_text'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Vote
        response = self.client.post(reverse('details', kwargs={'pk': 1}), {'choice': 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Checking if you can't vote for the second choice
        response = self.client.post(reverse('details', kwargs={'pk': 1}), {'choice': 2})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # If this vote was counted
        response = self.client.get(reverse('details', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['choices'][0]['votes']), 1)
        # Checking an unauthorized user
        self.client.credentials()
        response = self.client.post(reverse('details', kwargs={'pk': 1}), {'choice': 1})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_voting_type_1(self):
        self.client.login(username=self.client_data['username'],
                          password=self.client_data['password'])
        response = self.client.post(reverse('login'), self.client_data)
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        # Creating a new voting
        self.voting_data['type'] = 1
        response = self.client.post(reverse('list'), self.voting_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Creating a new choices
        response = self.client.put(reverse('details', kwargs={'pk': 1}), {'text': 'test_text'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.put(reverse('details', kwargs={'pk': 1}), {'text': 'test_text'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Vote
        response = self.client.post(reverse('details', kwargs={'pk': 1}), {'choice': 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Checking if you can vote for the second choice
        response = self.client.post(reverse('details', kwargs={'pk': 1}), {'choice': 2})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # If this vote was counted
        response = self.client.get(reverse('details', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['choices'][0]['votes']), 1)
        # Checking an unauthorized user
        self.client.credentials()
        response = self.client.post(reverse('details', kwargs={'pk': 1}), {'choice': 1})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

