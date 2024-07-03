from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework import generics, status, permissions
from .models import FriendRequest, User
from .serializers import FriendRequestSerializer, UserSearchSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.throttling import UserRateThrottle
from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)


class SearchPagination(PageNumberPagination):
    page_size = 10


class UserSearchView(generics.ListAPIView):
    serializer_class = UserSearchSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = SearchPagination

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        if '@' in query:
            return User.objects.filter(email__iexact=query)
        else:
            return User.objects.filter(username__icontains=query)
        
    def list(self, request, *args, **kwargs):
        
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response({"message": "No users found matching the query."}, status=status.HTTP_404_NOT_FOUND)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class FriendRequestThrottle(UserRateThrottle):
    rate = '3/minute'



User = get_user_model()


class SendFriendRequestView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerializer
    throttle_classes = [FriendRequestThrottle]

    def post(self, request, *args, **kwargs):
        to_user_id = request.data.get('to_user_id')
        from_user = request.user
       
        
        if from_user.id == int(to_user_id):
            return Response({"error": "You are not allowed to send friend request to Yourself"}, status=status.HTTP_400_BAD_REQUEST)

        if not to_user_id:
            return Response({"error": "to_user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            to_user = User.objects.get(id=to_user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user, status='pending').exists():
            return Response({"error": "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST)

        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user, status='accepted').exists():
            return Response({"error": "Already Friend...Cannot Send Friend request"}, status=status.HTTP_400_BAD_REQUEST)

        try:  
            friend_request = FriendRequest(from_user=from_user, to_user=to_user, status='pending')
            friend_request.save()
        except Exception as e:
            return Response({"error": "Failed to send friend request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Friend request sent"}, status=status.HTTP_201_CREATED)



@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def accept_friend_request(request, request_id):
    try:
        friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user)
        friend_request.status = 'accepted'
        friend_request.save()
        return Response({"message": "Friend request accepted"}, status=status.HTTP_200_OK)
    except FriendRequest.DoesNotExist:
        return Response({"message": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def reject_friend_request(request, request_id):
    try:
        friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user)
        friend_request.status= 'rejected'
        friend_request.save()
        return Response({"message": "Friend request rejected"}, status=status.HTTP_200_OK)
    except FriendRequest.DoesNotExist:
        return Response({"message": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND)

class ListFriendsView(generics.ListAPIView):
    serializer_class = UserSearchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(
            Q(sent_requests__to_user=self.request.user, sent_requests__status='accepted') |
            Q(received_requests__from_user=self.request.user, received_requests__status='accepted')
        ).distinct()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "No friends yet."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ListPendingRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status='pending')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
