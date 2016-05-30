from rest_framework import serializers

from users.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, min_length=6, max_length=32)

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            User.USERNAME_FIELD,
            'password',
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    @staticmethod
    def init_data(obj):
        return obj.value


class UserSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')
