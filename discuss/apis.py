from rest_framework import (
    viewsets,
    status
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from discuss.models import Discuss
from discuss.paginations import DiscussPagination
from discuss.serializers import DiscussSampleSerializer, GuestDiscussSerializer, DiscussSerializer


class DiscussViewSet(viewsets.GenericViewSet):
    serializer_class = DiscussSerializer
    permission_classes = [AllowAny, ]
    queryset = Discuss.objects.all()
    pagination_class = DiscussPagination

    def create(self, request, *args, **kwargs):
        # Guest 用户
        if request.user.is_anonymous():
            serializer = GuestDiscussSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            pass
        # 注册用户
        else:
            serializer = DiscussSampleSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            pass
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
