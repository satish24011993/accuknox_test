from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from ..models import FriendRequest, CustomUser

User = get_user_model()

class ViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Create users
        self.user26 = CustomUser.objects.create_user(
            email='user26@example.com', username='user26', password='Test@123'
        )
        self.user27 = CustomUser.objects.create_user(
            email='user27@example.com', username='user27', password='Test@123'
        )

        # Obtain tokens
        self.token1, _ = Token.objects.get_or_create(user=self.user26)
        self.token2, _ = Token.objects.get_or_create(user=self.user27)

    def test_signup(self):
        url = reverse('signup')
        data = {
            'email':'user28@example.com',
            'username':'user28',
            'password':'Test@123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 3)
    
    def test_login(self):
        url = reverse('login')
        data = {
            'email':'user26@example.com',
            'password': 'Test@123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
    
    def test_user_search_by_name(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token1.key)
        url = reverse('user-search')
        response = self.client.get(url + '?q=user', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) >= 2)
    
    def test_user_search_by_email(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token1.key)
        url = reverse('user-search')
        response = self.client.get(url+'?q=user26@example.com', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['email'],'user26@example.com')
    
    def test_send_friend_request(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token1.key)
        url = reverse('send-friend-request', kwargs={'user_id':self.user27.id})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(FriendRequest.objects.count(), 1)
        friend_request = FriendRequest.objects.first()
        self.assertEqual(friend_request.from_user, self.user26)
        self.assertEqual(friend_request.to_user, self.user27)
        self.assertEqual(friend_request.status, 'pending')


    def test_accept_friend_request(self):
        FriendRequest.objects.create(from_user=self.user26, to_user=self.user27)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token2.key)
        friend_request = FriendRequest.objects.first()
        url = reverse('respond-friend-request', kwargs={'request_id':friend_request.id})
        data = {'action':'accept'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        friend_request.refresh_from_db()
        self.assertEqual(friend_request.status, 'accepted')

    def test_reject_friend_request(self):
        FriendRequest.objects.create(from_user=self.user26, to_user=self.user27)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token2.key)
        friend_request = FriendRequest.objects.first()
        url = reverse('respond-friend-request', kwargs={'request_id':friend_request.id})
        data = {'action':'reject'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        friend_request.refresh_from_db()
        self.assertEqual(friend_request.status, 'rejected')

    def test_list_friends(self):
        FriendRequest.objects.create(from_user=self.user26, to_user=self.user27, status='accepted')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token1.key)
        url = reverse('friends-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['email'], 'user27@example.com')
    
    def test_list_pending_friend_requests(self):
        FriendRequest.objects.create(from_user=self.user26, to_user=self.user27)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token1.key)
        url = reverse('pending-friend-requests')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data['results']), 1)
        # self.assertEqual(response.data['results'][0]['from_user']['email'], 'user26@example.com')

    
    def test_throttling_friend_requests(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token1.key)
        url = reverse('send-friend-request', kwargs={'user_id':self.user27.id})

        # Send first request
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Send second request to a new user
        user29 = CustomUser.objects.create_user(
            email='user29@example.com', username='user29',password='Test@123'
        )
        url = reverse('send-friend-request', kwargs={'user_id':user29.id})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Send third request to another new user
        user30 = CustomUser.objects.create_user(
            email='user30@example.com',username='user30',password='Test@123'
        )
        url = reverse('send-friend-request', kwargs={'user_id':user30.id})
        response = self.client.post(url, format='json')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # # Send fourth request, should be throttled
        # user31 = CustomUser.objects.create_user(
        #     email='user31@example.com', username='user31', password='Test@123'
        # )
        # url = reverse('send-friend-request', kwargs={'user_id':user31.id})
        # response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertIn('detail', response.data)

