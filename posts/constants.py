class PostsStatus:
    UPDATED = 0
    WAIT_FOR_UPDATED = 1
    UN_ACTIVE = 2
    DIED = -1


POST_STATUS_CHOICES = (
    (PostsStatus.UPDATED, "已更新"),
    (PostsStatus.WAIT_FOR_UPDATED, "待更新"),
    (PostsStatus.UN_ACTIVE, "不活跃"),
    (PostsStatus.DIED, "404 死链"),
)
