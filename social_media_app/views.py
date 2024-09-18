from django.contrib.auth.models import User
from rest_framework import generics, status, permissions, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.db.models import Q
from .models import FriendRequest,Friend,CustomUser
from .serializers import UserSerializer, FriendRequestSerializer,FriendSerializer, UserRegistrationSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.utils.decorators import method_decorator

from django.contrib.auth import authenticate

# Rate limiter: Limit to 3 friend request per minute
class FriendRequestThrottle(UserRateThrottle):
    rate = '3/min'


# User Signup View
class SignupView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

# User Login view
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email,password=password)
        if user:
            token,_ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error':'Invalid Credentials'}, status=400)

class IsAuthenticate(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


# API for Searching Users by Email or Name (Paginated)
class UserSearchView(generics.ListAPIView):
    # queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10

    # @method_decorator(cache_page(60*5))
    def get_queryset(self):
        keyword = self.request.query_params.get('q','')
        if '@' in keyword: # Exact email match
            return CustomUser.objects.filter(email__iexact=keyword)
        else: # Search by name (partial match)
            return CustomUser.objects.filter(Q(username__icontains=keyword)|Q(first_name__icontains=keyword)|Q(last_name__icontains=keyword))

# Send Friend Request View
class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [FriendRequestThrottle]

    def post(self, request, user_id):
        # to_user = request.data.get('to_user_id')
        to_user = generics.get_object_or_404(CustomUser, id=user_id)
        # try:
        #     to_user = User.objects.get(id=to_user_id)
        #     if FriendRequest.objects.filter(from_user = request.user, to_user=to_user,
        #                                     is_accepted=False).exists():
        #         return Response({'error':'Friend request already send'}, status=status.HTTP_400_BAD_REQUEST)
        #     FriendRequest.objects.create(from_user=request.user, to_user=to_user)
        #     return Response({'message':'Friend request sent'}, status=status.HTTP_201_CREATED)
        # except User.DoesNotExist:
        #     return Response({'error':'User not found'}, status=status.HTTP_404_NOT_FOUND)
        if FriendRequest.objects.filter(from_user=request.user, to_user=to_user):
            return Response({'error':'Friend request already sent.'}, status=400)
        FriendRequest.objects.create(from_user=request.user, to_user=to_user)
        return Response({'status':'Friend request sent.'})
      

# List Friends View
class FriendsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    # def get_queryset(self):
    #     return Friend.objects.filter(user=self.request.user)
    def get_queryset(self):
        user = self.request.user
        # cache_key = f'friends_list_{user.id}'
        # friends = cache.get(cache_key)
        # if not friends:
        accepted_requests = FriendRequest.objects.filter(
            (Q(from_user=user)|Q(to_user=user)),
            status='accepted'
        ).select_related('from_user','to_user')
        friends = set()
        for req in accepted_requests:
            friends.add(req.from_user)
            friends.add(req.to_user)
        friends.discard(user)
        return list(friends)
    

# List Pending Friend Request View
class PendingFriendRequestsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, 
                                            status='pending'
                                            ).select_related('from_user','to_user')
    

class RespondFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id):
        action = request.data.get('action')
        friend_request = generics.get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
        if action == 'accept':
            friend_request.status = 'accepted'
            friend_request.save()
            return Response({'status':'Friend request accepted.'})
        elif action == 'reject':
            friend_request.status = 'rejected'
            friend_request.save()
            return Response({'status':'Friend request rejected.'})
        else:
            return Response({'error':'Invalid action.'}, status=400)
        