from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirmation = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'password_confirmation', 'bio')
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError("Passwords don't match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            bio=validated_data.get('bio', '')
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                    return data
                else:
                    raise serializers.ValidationError("User account is disabled.")
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'bio', 'profile_picture', 
                 'followers_count', 'following_count', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')