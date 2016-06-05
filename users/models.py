from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.db import models

from config.settings import DEFAULT_AVATAR
from .constants import PROVIDERS_CHOICES, ROLES_CHOICES, Roles, ALINK_VERIFY_CODE_LENGTH


class UserManager(BaseUserManager):
    def _create_user(self, username, email, role, password=None, avatar=None, is_superuser=False, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, is_superuser=is_superuser, avatar=avatar,
                          role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, avatar=None, **extra_fields):
        return self._create_user(username, email, password=password, role=Roles.Normal, avatar=avatar, **extra_fields)

    def create_superuser(self, username, email, password, avatar=None, **extra_fields):
        return self._create_user(username, email, password=password, role=Roles.Admin, avatar=avatar, is_superuser=True
                                 , **extra_fields)

    def create_guest(self, username, email, **extra_fields):
        return self._create_user(username, email, role=Roles.Guest, **extra_fields)


# Create your models here.
# 创建了自定义的User,也必须要创建自定义的UserManager
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('注册邮箱', unique=True, db_index=True)
    username = models.CharField('昵称', max_length=255, db_index=True, default='')

    score = models.IntegerField('积分', default=0)
    coin = models.IntegerField('硬币', default=0)

    is_staff = models.BooleanField('管理员', default=False)

    avatar = models.URLField('头像', max_length=255, default=DEFAULT_AVATAR)

    create_at = models.DateTimeField('创建时间', auto_now_add=True)

    alink_verify_code = models.CharField('激活链接验证码', max_length=ALINK_VERIFY_CODE_LENGTH, blank=True, null=True)

    last_alink_verify_time = models.DateTimeField('上一次激活链接发送请求验证码请求时间', blank=True, null=True)

    role = models.IntegerField('角色', choices=ROLES_CHOICES, default=Roles.Guest)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    # '-' 表示倒序
    class Meta:
        ordering = ['-id']

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return "%s (%s)" % (self.username, self.email)

    def is_guest(self):
        return self.role == Roles.Guest

    def __str__(self):
        return "%s(%s)" % (self.username, self.email)


class OauthManager(BaseUserManager):
    def create_oauth(self, username, email, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        email = self.normalize_email(email)
        oauth = self.model(
            username=username, email=email, **extra_fields)
        oauth.save(using=self._db)
        return oauth


# 每个Oauth绑定的帐户都算是一个小的子帐户,拥有从第三方平台获取到的 :
# username, email, avatar_url, expire, access_token ,refresh_token, provider
# 并绑定了一个标准用户对象
class Oauth(models.Model):
    username = models.CharField('名称', max_length=32, blank=True)
    email = models.EmailField('邮箱', db_index=True)
    avatar_url = models.URLField('头像url', max_length=255, blank=True)

    expire_at = models.DateTimeField('token失效时间', blank=True, null=True)

    access_token = models.CharField('access_token', max_length=255, blank=True, null=True)
    refresh_token = models.CharField('refresh_token', max_length=255, blank=True, null=True)

    provider = models.IntegerField('类别', choices=PROVIDERS_CHOICES)
    user = models.ForeignKey(User, null=True, blank=True)

    objects = OauthManager()
