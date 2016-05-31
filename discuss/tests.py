from django.test import TestCase

from discuss.models import Discuss
from sendcloud.constants import SendCloudTemplates
from sendcloud.utils import sendcloud_template
from users.models import User


class DiscussTestCase(TestCase):
    def setUp(self):
        self.email = '670425438@qq.com'
        self.username = 'joway'

    def test_discuss(self):
        sendcloud_template(to=[self.email],
                           tpt_ivk_name=SendCloudTemplates.Test,
                           sub_vars={'name': [self.username]})
        user = User.objects.create_guest(username=self.username,
                                         email=self.email)
        discuss = Discuss.objects.create_discuss(user=user, content='Test content',
                                                 post_url='http:baidu.com/123.json')
        print(user)
        print(discuss)
