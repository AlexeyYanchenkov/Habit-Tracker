from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'email',
            'avatar',
            'phone',
            'country',
            'telegram_chat_id',
            'is_active',
            'is_staff',
            'date_joined',
        )
        read_only_fields = ('id', 'email', 'is_active', 'is_staff', 'date_joined')

    def validate_telegram_chat_id(self, value):
        return value


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'  # указываем, что поле для логина - email

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError('No active account found with the given credentials')

        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')

        refresh = self.get_token(user)

        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'email': user.email,
        }
        return data


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'avatar', 'phone', 'country', 'telegram_chat_id')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
