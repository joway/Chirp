# coding=utf-8
from rest_framework import serializers

from discuss.models import Discuss
from users.serializers import UserSampleSerializer


class DiscussSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discuss


class DiscussSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discuss
        fields = ('content',)


class GuestDiscussSerializer(serializers.ModelSerializer):
    user = UserSampleSerializer()

    class Meta:
        model = Discuss
        fields = ('content', 'user')
