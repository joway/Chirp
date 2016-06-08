# from discuss.apis import DiscussViewSet
# from utils.tests import DjangoTestCase
#
#
# class DiscussTestCase(DjangoTestCase):
#     def setUp(self):
#         super().setUp()
#         self.base_url = '/discuss/'
#
#     def test_a_register(self):
#         viewset = DiscussViewSet.as_view(actions={'post': 'create'})
#         data = {
#             'username': self.username,
#             'email': self.email,
#             'post_url': self.post_url,
#             'content': 'xxxxxxxxxxxx',
#             'reply_to_id': '1'
#         }
#         request = self.factory.post(self.base_url + 'discuss/', data=data)
#         response = viewset(request)
#         print(response.data)
#         self.assertEqual(response.status_code, 201)
