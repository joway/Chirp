from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from config.settings import DOMAIN_URL
from sendcloud.constants import SendCloudTemplates
from sendcloud.utils import sendcloud_template
from users.constants import MAX_MAIL_INTERVAL_SECONDS, ALINK_VERIFY_CODE_LENGTH, Roles
from users.models import User
from users.serializers import UserSerializer
from utils.jwt import get_jwt_token
from utils.utils import get_random_string


class UserService(object):
    @classmethod
    def login(cls, email, password):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(data={'message': '404001 用户未注册'}, status=status.HTTP_404_NOT_FOUND)
        if user.check_password(password):
            token = get_jwt_token(user)
            return Response({'jwt': token, 'user': UserSerializer(user).data}, status=status.HTTP_200_OK)
        else:
            return Response(data={'message': '401001 密码错误'}, status=status.HTTP_401_UNAUTHORIZED)

    @classmethod
    def register(cls, email, username):
        user, is_create = User.objects.get_or_create(email=email)
        if not is_create:
            return Response(data={'message': '400001 email已存在'}, status=status.HTTP_400_BAD_REQUEST)

        if user.last_alink_verify_time and (
                    timezone.now() - user.last_alink_verify_time).seconds < MAX_MAIL_INTERVAL_SECONDS:
            return Response(data={'message': '403002 验证码请求过于频繁'}, status=status.HTTP_403_FORBIDDEN)

        user.username = username
        user.alink_verify_code = get_random_string(ALINK_VERIFY_CODE_LENGTH)
        if sendcloud_template(to=[email],
                              tpt_ivk_name=SendCloudTemplates.REGISTER,
                              sub_vars={'%username%': [username],
                                        '%url%': [DOMAIN_URL + '/user/activate?confirm=' + user.alink_verify_code]}):
            user.save()
            return Response(data={'message': '注册成功'}, status=status.HTTP_200_OK)
        return Response(data={'message': '403003 邮件发送失败'}, status=status.HTTP_403_FORBIDDEN)

    @classmethod
    def registerpwd(cls, email, password):
        user, is_create = User.objects.get_or_create(email=email)
        if not is_create:
            return Response(data={'message': '400001 email已存在'}, status=status.HTTP_400_BAD_REQUEST)

        if user.last_alink_verify_time and (
                    timezone.now() - user.last_alink_verify_time).seconds < MAX_MAIL_INTERVAL_SECONDS:
            return Response(data={'message': '403002 验证码请求过于频繁'}, status=status.HTTP_403_FORBIDDEN)

        user.username = email[:email.find('@')]
        user.set_password(password)
        user.alink_verify_code = get_random_string(ALINK_VERIFY_CODE_LENGTH)
        if sendcloud_template(to=[email],
                              tpt_ivk_name=SendCloudTemplates.REGISTER,
                              sub_vars={'%username%': [email],
                                        '%url%': [DOMAIN_URL + '/user/activate?confirm=' + user.alink_verify_code]}):
            user.save()
            return Response(data={'message': '注册成功, 已发送验证邮件'}, status=status.HTTP_200_OK)
        return Response(data={'message': '403003 邮件发送失败'}, status=status.HTTP_403_FORBIDDEN)

    @classmethod
    def init(cls, email, password):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(data={'message': '404001 用户不存在'}, status=status.HTTP_404_NOT_FOUND)
        if user.password:
            return Response(data={'message': '400001 用户已初始化'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
        user.save()
        return Response(data={'message': '初始化成功'}, status=status.HTTP_200_OK)

    @classmethod
    def logout(cls):
        pass

    @classmethod
    def confirm(cls, confirm):
        try:
            user = User.objects.get(alink_verify_code=confirm)
        except User.DoesNotExist:
            return Response(data={'message': '403001 链接无效'}, status=status.HTTP_403_FORBIDDEN)

        if user.alink_verify_code == confirm:
            user.alink_verify_code = None
            user.role = Roles.Normal
            user.save()
            return Response(data={'message': '激活成功'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'message': '403001 激活链接失效'}, status=status.HTTP_403_FORBIDDEN)

    @classmethod
    def bind_oauth(cls, user, oauth):
        oauth.user = user
        oauth.save()
        return oauth
