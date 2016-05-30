# coding=utf-8
from rest_framework import serializers

from discuss.models import Discuss
from posts.models import Post
from users.serializers import UserSampleSerializer


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post


class PostSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('content',)


class PostUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('url',)

