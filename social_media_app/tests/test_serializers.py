from django.test import TestCase
from ..serializers import UserSerializer, FriendRequestSerializer
from django.contrib.auth import get_user_model
from ..models import FriendRequest, CustomUser

User = get_user_model()

class SerializerTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='user34@example.com', username='user34', password='Test@123'
        )

    def test_user_serializer(self):
        serializer = UserSerializer(instance=self.user)
        data = serializer.data
        self.assertEqual(data['email'],'user34@example.com')
        self.assertEqual(data['username'], 'user34')

    def test_friend_request_serializer(self):
        other_user = CustomUser.objects.create_user(
            email='other@example.com', username='other', password='Test@123'
        )
        friend_request = FriendRequest.objects.create(
            from_user = self.user, to_user=other_user
        )
        serializer = FriendRequestSerializer(instance=friend_request)
        data = serializer.data
        self.assertEqual(data['from_user']['email'], 'user34@example.com')
        self.assertEqual(data['to_user']['email'],'other@example.com')
        self.assertEqual(data['status'],'pending')