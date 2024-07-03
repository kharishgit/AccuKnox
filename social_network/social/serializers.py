from rest_framework import serializers
from .models import User,FriendRequest
from django.contrib.auth import authenticate,get_user_model
from django.core.exceptions import ValidationError
from django.db.models import Q
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email

    def create(self, validated_data):
        validated_data['email'] = validated_data['email'].lower()
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')

       
        user = authenticate(username=email, password=password)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid Credentials")


class FriendRequestSerializer(serializers.ModelSerializer):
    from_name=serializers.SerializerMethodField()
    class Meta:
        model = FriendRequest
        fields = '__all__'
    
    def get_from_name(self, obj):
        if obj.from_user is not None:
            return obj.from_user.username
        else:
            return None

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# class FriendSerializer(serializers.ModelSerializer):
#     from_user = serializers.SerializerMethodField()
#     to_user = serializers.SerializerMethodField()

#     class Meta:
#         model = FriendRequest
#         fields = ['id', 'from_user', 'to_user', 'timestamp', 'status']

#     def get_from_user(self, obj):
#         return UserSerializer(obj.from_user).data

#     def get_to_user(self, obj):
#         return UserSerializer(obj.to_user).data


class UserSearchSerializer(serializers.ModelSerializer):
    friends = serializers.SerializerMethodField()
    # sent_requests = FriendSerializer(many=True,read_only=True)
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email','friends']

    def get_friends(self, obj):
        friends = User.objects.filter(
            Q(sent_requests__to_user=obj, sent_requests__status='accepted') |
            Q(received_requests__from_user=obj, received_requests__status='accepted')
        ).distinct()

        return FriendSerializer(friends, many=True).data
