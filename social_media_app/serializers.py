# from django.contrib.auth.models import User
from rest_framework import serializers
# from .models import CustomUser, FriendRequest, Friendship, Friend
from .models import FriendRequest, Friend,CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only = True)
    to_user = UserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status', 'timestamp']


class FriendSerializer(serializers.ModelSerializer):
    friend = UserSerializer()

    class Meta:
        model = Friend
        fields = ['friend']