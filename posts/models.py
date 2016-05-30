from django.db import models

# Create your models here.
from config.settings import POSTS_UUID_LENGTH
from posts.constants import POST_STATUS_CHOICES, PostsStatus
from utils.utils import get_uuid, format_url


def post_unique_uuid():
    uuid = get_uuid(POSTS_UUID_LENGTH)
    while Post.objects.filter(id=uuid).exists():
        uuid = get_uuid(POSTS_UUID_LENGTH)
    return uuid


class PostManager(models.Manager):
    def get_or_create_with_url(self, post_url):
        return self.get_or_create(url=format_url(post_url))


class Post(models.Model):
    id = models.CharField('uuid', max_length=POSTS_UUID_LENGTH,
                          default=post_unique_uuid, primary_key=True,
                          editable=False)
    author = models.CharField(max_length=16, null=True, blank=True)
    title = models.CharField(max_length=32, null=True, blank=True)
    content = models.TextField(blank=True, null=True)

    url = models.URLField('链接')

    score = models.IntegerField('评分', default=0)
    create_at = models.DateTimeField(null=True, blank=True)

    last_scanned = models.DateTimeField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    status = models.IntegerField(choices=POST_STATUS_CHOICES,
                                 default=PostsStatus.WAIT_FOR_UPDATED)

    objects = PostManager()

    # def __str__(self):
    #     return self.url
    #
    # def __repr__(self):
    #     return self.url
