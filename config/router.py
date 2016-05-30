from rest_framework import routers

# from payment.apis import PaymentViewSet
from discuss.apis import DiscussViewSet

router = routers.DefaultRouter(trailing_slash=True)

router.register(r"discuss", DiscussViewSet, base_name="discuss")
# router.register(r"user", UserViewSet, base_name="user")
