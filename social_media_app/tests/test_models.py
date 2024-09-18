from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import FriendRequest, CustomUser
from django.db import IntegrityError

User = get_user_model()

class ModelTests(TestCase):

    def setUp(self):
        self.user32 = CustomUser.objects.create_user(
            email='user32@example.com', username='user32', password='Test@123'
        )
        self.user33 = CustomUser.objects.create_user(
            email='user33@example.com', username='user33', password='Test@123'
        )

    def test_friend_request_creation(self):
        friend_request = FriendRequest.objects.create(
            from_user=self.user32, to_user=self.user33
        )
        self.assertEqual(friend_request.status, 'pending')
        self.assertEqual(friend_request.from_user, self.user32)
        self.assertEqual(friend_request.to_user, self.user33)
    
    def test_friend_request_unique_constraint(self):
        FriendRequest.objects.create(from_user=self.user32, to_user=self.user33)
        with self.assertRaises(IntegrityError):
            # Should raise an IntegrityError due to unique_together constraint
            FriendRequest.objects.create(from_user=self.user32, to_user=self.user33)