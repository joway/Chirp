import shortuuid
from django.db import models

# Create your models here.
from config.settings import DISCUSS_UUID_LENGTH
from discuss.constants import DISCUSS_STATUS_CHOICES, DiscussStatus
from posts.models import Post
from users.models import User


def discuss_unique_uuid():
    shortuuid.set_alphabet('0123456789ABCDEFGHJKLMNPQRSTUVWXYZ')
    uuid = shortuuid.uuid()[:DISCUSS_UUID_LENGTH]
    while Discuss.objects.filter(id=uuid).exists():
        uuid = shortuuid.uuid()[:DISCUSS_UUID_LENGTH]
    return uuid


class DiscussManager(models.Manager):
    def create_discuss(self, user, content):
        if user.is_guest():
            self.create(user=user, content=content, status=DiscussStatus.WAIT_FOR_APPROVED)
        else:
            self.create(user=user, content=content, status=DiscussStatus.AUTHORIZED)


class Discuss(models.Model):
    id = models.CharField('uuid', max_length=DISCUSS_UUID_LENGTH,
                          default=discuss_unique_uuid, primary_key=True,
                          editable=False)
    content = models.TextField(max_length=1024, blank=True)
    create_at = models.DateTimeField(auto_created=True)
    user = models.ForeignKey(User)
    status = models.IntegerField(choices=DISCUSS_STATUS_CHOICES)

    post = models.ForeignKey(Post)

    object = DiscussManager()
