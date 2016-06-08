from rest_framework import routers

# from payment.apis import PaymentViewSet
from discuss.apis import DiscussViewSet
from upload.apis import UploadViewSet
from users.apis import UserViewSet, SocialAuthViewSet

router = routers.DefaultRouter(trailing_slash=True)

router.register(r"discuss", DiscussViewSet, base_name="discuss")
router.register(r"user", UserViewSet, base_name="user")
router.register(r"upload", UploadViewSet, base_name="upload")
# router.register(r"oauth", SocialAuthViewSet, base_name="oauth")
