from django.db import models

# Create your models here.
from config.settings import DISCUSS_UUID_LENGTH
from discuss.constants import DISCUSS_STATUS_CHOICES, DiscussStatus
from posts.models import Post
from users.models import User
from utils.utils import get_uuid


def discuss_unique_uuid():
    uuid = get_uuid(DISCUSS_UUID_LENGTH)
    while Discuss.objects.filter(id=uuid).exists():
        uuid = get_uuid(DISCUSS_UUID_LENGTH)
    return uuid


class DiscussManager(models.Manager):
    def create_discuss(self, user, content, post_url):
        if user.is_guest():
            return self.create(user=user, content=content,
                               status=DiscussStatus.WAIT_FOR_APPROVED,
                               post=Post.objects.get_or_create_with_url(post_url=post_url)[0])
        else:
            return self.create(user=user, content=content, status=DiscussStatus.AUTHORIZED,
                               post=Post.objects.get_or_create_with_url(post_url=post_url)[0])


class Discuss(models.Model):
    id = models.CharField('uuid', max_length=DISCUSS_UUID_LENGTH,
                          default=discuss_unique_uuid, primary_key=True,
                          editable=False)
    content = models.TextField(max_length=1024, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    status = models.IntegerField(choices=DISCUSS_STATUS_CHOICES)

    post = models.ForeignKey(Post)

    objects = DiscussManager()
