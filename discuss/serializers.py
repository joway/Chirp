# coding=utf-8
from rest_framework import serializers

from discuss.models import Discuss
from posts.serializers import PostUrlSerializer


class DiscussSerializer(serializers.ModelSerializer):
    post = PostUrlSerializer()

    class Meta:
        model = Discuss


class CreateDiscussSerializer(serializers.ModelSerializer):
    post_url = serializers.URLField()


class DiscussAuthCreateSerializer(CreateDiscussSerializer):
    class Meta:
        model = Discuss
        fields = ('content', 'post_url')


class GuestDiscussCreateSerializer(CreateDiscussSerializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=32)

    class Meta:
        model = Discuss
        fields = ('content', 'email', 'username', 'post_url')
