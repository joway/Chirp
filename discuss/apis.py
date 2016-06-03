from django.db.transaction import non_atomic_requests
from rest_framework import (
    viewsets,
    status
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from discuss.models import Discuss
from discuss.paginations import DiscussPagination
from discuss.serializers import DiscussAuthCreateSerializer, GuestDiscussCreateSerializer, DiscussSerializer
from sendcloud.constants import SendCloudTemplates
from sendcloud.utils import sendcloud_template
from users.models import User


class DiscussViewSet(viewsets.GenericViewSet):
    serializer_class = DiscussSerializer
    permission_classes = [AllowAny, ]
    queryset = Discuss.objects.all()
    pagination_class = DiscussPagination

    @non_atomic_requests
    def create(self, request, *args, **kwargs):
        # Guest 用户
        if request.user.is_anonymous():
            serializer = GuestDiscussCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # reply_to_id =
            if not User.objects.filter(email=serializer.data['email']).exists():
                if sendcloud_template(to=[serializer.data['email']],
                                      tpt_ivk_name=SendCloudTemplates.Test,
                                      sub_vars={'name': [serializer.data['username']]}):
                    user = User.objects.create_guest(serializer.data['username'],
                                                     serializer.data['email'])
                    discuss = Discuss.objects.create_discuss(user=user, content=serializer.data['content'],
                                                             post_url=serializer.data['post_url'])
                else:
                    return Response({'message', '403001 发送验证邮件失败'},
                                    status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({'message', '403002 用户已注册, 请先登陆'},
                                status=status.HTTP_403_FORBIDDEN)
        # 注册用户
        else:
            serializer = DiscussAuthCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            discuss = Discuss.objects.create_discuss(user=request.user,
                                                     content=serializer.data['content'],
                                                     post_url=serializer.data['post_url'])
        return Response(self.get_serializer(instance=discuss).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'message': '删除成功'}, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': '修改成功'}, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
