# coding=utf-8
from rest_framework import serializers

from discuss.models import Discuss
from posts.serializers import PostUrlSerializer
from users.serializers import UserSerializer


class DiscussSerializer(serializers.ModelSerializer):
    post = PostUrlSerializer()
    user = UserSerializer()

    class Meta:
        model = Discuss


class CreateDiscussSerializer(serializers.ModelSerializer):
    post_url = serializers.URLField()


class DiscussAuthCreateSerializer(CreateDiscussSerializer):
    class Meta:
        model = Discuss
        fields = ('content', 'post_url', 'reply_to', 'parent_id')


class GuestDiscussCreateSerializer(CreateDiscussSerializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=32)
    reply_to = serializers.RelatedField(source='reply_to', read_only=True)

    class Meta:
        model = Discuss
        fields = ('content', 'email', 'username', 'post_url',
                  'reply_to', 'parent_id')
