"""
Django settings for Discuss project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import datetime
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

try:
    from .local_settings import *
except ImportError:
    pass

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # local apps
    'discuss',
    'users',
    'posts',
    'upload',

    # third part apps
    'rest_framework',
    'jet.dashboard',
    'jet',
    'social.apps.django_app.default',
    'corsheaders',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
)
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = (
#     'hostname.example.com'
# )

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            'ATOMIC_REQUESTS': True
        }
    }
else:
    DATABASES = {
        'default': {
            'NAME': os.environ.get('MYSQL_INSTANCE_NAME', 'xxx'),
            'ENGINE': 'django.db.backends.mysql',
            'USER': os.environ.get("MYSQL_USERNAME", 'xxx'),
            'PASSWORD': os.environ.get("MYSQL_PASSWORD", 'xxx'),
            'HOST': os.environ.get("MYSQL_HOST", 'xxx'),
            'PORT': os.environ.get("MYSQL_PORT", 3306),
        },
    }

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
TIME_ZONE = 'Asia/Shanghai'

LANGUAGE_CODE = 'zh-hans'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
STATIC_URL = 'http://o6yjiddjp.bkt.clouddn.com/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "cdn")

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
}

JWT_AUTH = {
    'JWT_ENCODE_HANDLER': 'rest_framework_jwt.utils.jwt_encode_handler',
    'JWT_DECODE_HANDLER': 'rest_framework_jwt.utils.jwt_decode_handler',
    'JWT_PAYLOAD_HANDLER': 'rest_framework_jwt.utils.jwt_payload_handler',
    'JWT_PAYLOAD_GET_USER_ID_HANDLER': 'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'rest_framework_jwt.utils.jwt_response_payload_handler',
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=10),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,
    'JWT_ALLOW_REFRESH': False,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}

DISCUSS_UUID_LENGTH = 12
POSTS_UUID_LENGTH = 12

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = (
    'social.backends.qq.QQOAuth2',
    'social.backends.github.GithubOAuth2',
    'users.oauth.CodingOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

DOMAIN_URL = 'http://chirp.i2p.pub'

# mail : sendcloud
EMAIL_BACKEND = 'sendcloud.SendCloudBackend'
DEFAULT_FROM_EMAIL = 'admin@joway.wang'
MAIL_DEBUG = False
MAIL_APP_USER = os.environ.get('MAIL_APP_USER')
MAIL_APP_KEY = os.environ.get('MAIL_APP_KEY')

# oauth
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'email']

SOCIAL_AUTH_USER_MODEL = 'users.Oauth'

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
)

SOCIAL_AUTH_GITHUB_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_GITHUB_SCOPE = [
    'user'
]

# re url
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/done/'

# oauth
SOCIAL_AUTH_QQ_KEY = os.environ.get('SOCIAL_AUTH_QQ_KEY')
SOCIAL_AUTH_QQ_SECRET = os.environ.get('SOCIAL_AUTH_QQ_SECRET')

SOCIAL_AUTH_GITHUB_KEY = os.environ.get('SOCIAL_AUTH_GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = os.environ.get('SOCIAL_AUTH_GITHUB_SECRET')

SOCIAL_AUTH_CODING_KEY = os.environ.get('SOCIAL_AUTH_CODING_KEY')
SOCIAL_AUTH_CODING_SECRET = os.environ.get('SOCIAL_AUTH_CODING_SECRET')

DEFAULT_AVATAR = 'https://dn-joway.qbox.me/1465087838481_user_116px_1196112_easyicon.net.png'

QINIU_ACCESS_KEY = os.environ.get('QINIU_ACCESS_KEY', 'xxx')
QINIU_SECRET_KEY = os.environ.get('QINIU_SECRET_KEY', 'xxx')
