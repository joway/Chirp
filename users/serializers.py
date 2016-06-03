from rest_framework import serializers

from users.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ('email', 'username')


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)


class UserActivateSerializer(serializers.Serializer):
    confirm = serializers.CharField(max_length=32)


class UserSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'avatar', 'id')
