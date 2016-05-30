class Providers:
    Github = 0
    QQ = 1
    Coding = 2
    Sina = 3

PROVIDERS_CHOICES = (
    (Providers.Github, "Github"),
    (Providers.QQ, "QQ"),
    (Providers.Coding, "Coding"),
    (Providers.Sina, "新浪微博"),
)


class Roles:
    Admin = 0
    Normal = 1
    Guest = 2

ROLES_CHOICES = (
    (Roles.Admin, "管理员"),
    (Roles.Normal, "普通用户"),
    (Roles.Guest, "访客"),
)

