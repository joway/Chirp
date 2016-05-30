import shortuuid
from django.db import models

# Create your models here.
from config.settings import POSTS_UUID_LENGTH
from posts.constants import POST_STATUS_CHOICES


def post_unique_uuid():
    shortuuid.set_alphabet('0123456789ABCDEFGHJKLMNPQRSTUVWXYZ')
    uuid = shortuuid.uuid()[:POSTS_UUID_LENGTH]
    while Post.objects.filter(id=uuid).exists():
        uuid = shortuuid.uuid()[:POSTS_UUID_LENGTH]
    return uuid


class Post(models.Model):
    id = models.CharField('uuid', max_length=POSTS_UUID_LENGTH,
                          default=post_unique_uuid, primary_key=True,
                          editable=False)
    author = models.CharField(max_length=16)
    title = models.CharField(max_length=32)
    content = models.TextField(blank=True)

    url = models.URLField('链接')

    score = models.IntegerField('评分', default=0)
    create_at = models.DateTimeField(null=True, blank=True)

    last_scanned = models.DateTimeField()
    last_updated = models.DateTimeField(auto_now=True)

    status = models.IntegerField(choices=POST_STATUS_CHOICES)
