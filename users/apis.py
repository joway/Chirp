from django.contrib.auth import login
from django.db.transaction import non_atomic_requests
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_encode_handler
from social.apps.django_app.utils import load_strategy, psa

from users.constants import Providers
from users.services import UserService
from utils.permissions import IsBound
from .models import User, Oauth
from .serializers import UserRegistrationSerializer, UserSerializer, UserLoginSerializer, \
    UserRegistrationWithPWDSerializer, SocialAuthSerializer


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
    def registerpwd(self, request):
        """
        注册
        """
        serializer = UserRegistrationWithPWDSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return UserService.registerpwd(email=serializer.data['email'], password=serializer.data['password'])

    @list_route(methods=['post'])
    @non_atomic_requests
    def init(self, request):
        """
        初始化密码
        """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return UserService.init(serializer.data['email'], serializer.data['password'])

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

    @list_route(methods=['get'], permission_classes=[IsAuthenticated, ])
    def detail(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)

    @list_route(methods=['get'], permission_classes=[AllowAny, ])
    def oauth(self, request, *args, **kwargs):
        data = request.data
        print(request.user)
        print(request.GET['next'])
        return Response(data=data, status=status.HTTP_200_OK)


class SocialAuthViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny, ]
    serializer_class = SocialAuthSerializer

    @list_route(methods=['post'], permission_classes=[IsAuthenticated, ])
    def bind(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        oauth = Oauth.objects.create(access_token=serializer.data['access_token'], user=user, provider=Providers.Github)
        strategy = load_strategy(request=request)
        kwargs = dict({(k, i) for k, i in serializer.data.items() if k != 'backend'})
        # 使用者驗證
        tmp = strategy.backend.do_auth(**kwargs)
        return Response(data={'message': '绑定成功'}, status=status.HTTP_200_OK)

    @list_route(methods=['post'], permission_classes=[IsBound, ])
    def login(self, request, *args, **kwargs):
        # payload = jwt_payload_handler(user)
        return Response({'jwt': jwt_encode_handler(payload), 'username': user.username})  # 回傳JWT token及使用者帳號

    @list_route(methods=['get'])
    @psa('social:complete')
    def register_by_access_token(self, request, backend):
        # This view expects an access_token GET parameter, if it's needed,
        # request.backend and request.strategy will be loaded with the current
        # backend and strategy.
        token = request.GET.get('access_token')
        user = request.backend.do_auth(token=token)
        if user:
            login(request, user)
            return 'OK'
        else:
            return 'ERROR'


@psa('social:complete')
def register_by_access_token(request, backend):
    # This view expects an access_token GET parameter, if it's needed,
    # request.backend and request.strategy will be loaded with the current
    # backend and strategy.
    token = request.GET.get('access_token')
    print(token)
    user = request.backend.do_auth(token)
    if user:
        login(request, user)
        return 'OK'
    else:
        return 'ERROR'
