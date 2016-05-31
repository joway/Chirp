from django.db.transaction import non_atomic_requests
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


from users.services import UserService
from .models import User
from .serializers import UserRegistrationSerializer, UserSerializer, UserLoginSerializer, UserActivateSerializer


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny, ]

    @list_route(methods=['post'])
    @non_atomic_requests
    def register(self, request):
        """
        注册
        """
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return UserService.register(email=serializer.data['email'], username=serializer.data['username'])

    @list_route(methods=['post'])
    @non_atomic_requests
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return UserService.login(serializer.data['email'], serializer.data['password'])

    @list_route(methods=['get'])
    @non_atomic_requests
    def activate(self, request):
        try:
            confirm = request.GET['confirm']
        except MultiValueDictKeyError:
            return Response(data={'message': '400001 格式非法'}, status=status.HTTP_400_BAD_REQUEST)
        return UserService.confirm(confirm)
