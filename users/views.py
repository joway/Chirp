from django.shortcuts import render
from rest_framework import permissions
from rest_framework import viewsets
import logging
from users.models import User
from users.serializers import UserSerializer

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


