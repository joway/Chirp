# from django.test import TestCase
#
# # Create your tests here.
# from rest_framework.test import APIRequestFactory
#
# from config.settings import JWT_AUTH
# from users.apis import UserViewSet
# from users.models import User
# from utils.utils import get_random_string
#
#
# class UserTestCase(TestCase):
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.base_url = '/user/'
#         self.username = 'joway'
#         self.email = '670425438@qq.com'
#         self.password = 'password'
#
#         self.settings(EMAIL_BACKEND='sendcloud.SendCloudBackend',
#                       MAIL_APP_USER='jowaywong',
#                       MAIL_APP_KEY='fwPcJDvCdgEHsuLt',
#                       DEFAULT_FROM_EMAIL='admin@joway.wang',
#                       JWT_AUTH=JWT_AUTH)
#
#     def test_a_register(self):
#         viewset = UserViewSet.as_view(actions={'post': 'register'})
#         data = {
#             'username': self.username,
#             'email': self.email
#         }
#         request = self.factory.post(self.base_url + 'register/', data=data)
#         response = viewset(request)
#         print(response.data)
#         self.assertEqual(response.status_code, 200)
#
#         request = self.factory.post(self.base_url + 'register/', data=data)
#         response = viewset(request)
#         print(response.data)
#
#         # 验证码请求过于频繁
#         self.assertEqual(response.status_code, 400)
#
#     def test_b_confirm(self):
#         viewset = UserViewSet.as_view(actions={'get': 'activate'})
#         self.user = User.objects.create_guest(username=self.username,
#                                               email=self.email,
#                                               alink_verify_code=get_random_string(32))
#         data = {
#             'confirm': self.user.alink_verify_code
#         }
#         request = self.factory.get(self.base_url + 'activate/', data=data)
#         response = viewset(request)
#         print(response.data)
#         # self.assertEqual(response.status_code, 200)
#
#     def test_c_login(self):
#         # viewset = UserViewSet.as_view(actions={'post': 'login'})
#         # user = User.objects.create_guest(username=self.username,
#         #                                  email=self.email,
#         #                                  alink_verify_code=get_random_string(32))
#         # user.set_password(self.password)
#         # user.save()
#         # data = {
#         #     'email': self.email,
#         #     'password': self.password
#         # }
#         # request = self.factory.post(self.base_url + 'login/', data=data)
#         # response = viewset(request)
#         # print(response.data)
#         # self.assertEqual(response.status_code, 200)
