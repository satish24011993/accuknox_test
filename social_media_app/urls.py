from django.urls import path
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from .views import SendFriendRequest, AcceptFriendRequest,RejectFriendRequest, ListFriends,DeleteFriend
from .views import SignupView,UserSearchView, SendFriendRequestView, FriendsListView,PendingFriendRequestsView, RespondFriendRequestView,LoginView


urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('friends/', FriendsListView.as_view(), name='friends-list'),
    path('friend-requests/',PendingFriendRequestsView.as_view(), name='pending-friend-requests'),
    path('send-friend-request/<int:user_id>/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('respond-friend-request/<int:request_id>/',
         RespondFriendRequestView.as_view(), name='respond-friend-request')
    # path('send_friend_request/', SendFriendRequestView.as_view(), name='send_friend_request'),
    # path('accept_friend_request/', AcceptFriendRequestView.as_view(), name='accept_friend_request'),
    # path('reject_friend_request/', RejectFriendRequestView.as_view(), name='reject_friend_request'),
    # path('friends/', FriendsListView.as_view(), name='friends_list'),
    # path('pending_requests/', PendingFriendRequestsView.as_view(), name='pending_requests'),
]