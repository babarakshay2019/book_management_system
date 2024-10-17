from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError

CustomUser = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'user_type', 'created_at', 'updated_at', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            user_type=validated_data['user_type']
        )
        return user

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)

    def validate(self, attrs):
        # Ensure the refresh token is present
        refresh_token = attrs.get('refresh_token')
        if not refresh_token:
            raise ValidationError("Refresh token is required.")
        return attrs

    def save(self):
        try:
            # Blacklist the refresh token
            token = RefreshToken(self.validated_data['refresh_token'])
            token.blacklist()
        except Exception:
            raise ValidationError("Invalid refresh token.")
