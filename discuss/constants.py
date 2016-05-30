class DiscussStatus:
    AUTHORIZED = 0
    WAIT_FOR_APPROVED = 1
    APPROVED = 2
    REJECTED = -1
    DELETED = -2


DISCUSS_STATUS_CHOICES = (
    (DiscussStatus.AUTHORIZED, "验证用户评论"),
    (DiscussStatus.WAIT_FOR_APPROVED, "待批准"),
    (DiscussStatus.APPROVED, "已批准"),
    (DiscussStatus.REJECTED, "被拒绝"),
    (DiscussStatus.DELETED, "被删除"),
)
