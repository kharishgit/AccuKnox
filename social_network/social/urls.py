from django.urls import path
from .views import *
    

    

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('friend-request/send/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('friend-request/accept/<int:request_id>/', accept_friend_request, name='accept-friend-request'),
    path('friend-request/reject/<int:request_id>/', reject_friend_request, name='reject-friend-request'),
    path('friends/', ListFriendsView.as_view(), name='list-friends'),
    path('friend-requests/', ListPendingRequestsView.as_view(), name='list-pending-requests'),
]