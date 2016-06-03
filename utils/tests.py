from django.test import TestCase


# Create your tests here.
from rest_framework.test import APIRequestFactory

from config.settings import JWT_AUTH


class DjangoTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.username = 'joway'
        self.email = '670425438@qq.com'
        self.password = 'password'
        self.post_url = 'http://baidu.com'

        self.settings(EMAIL_BACKEND='sendcloud.SendCloudBackend',
                      MAIL_APP_USER='jowaywong',
                      MAIL_APP_KEY='fwPcJDvCdgEHsuLt',
                      DEFAULT_FROM_EMAIL='admin@joway.wang',
                      JWT_AUTH=JWT_AUTH)
