from django.core.mail import EmailMessage


class SendCloudEmailMessage(EmailMessage):
    def __init__(self, to, template_invoke_name=None, sub_vars=None):
        super().__init__(to=to)
        self.to = to
        self.template_invoke_name = template_invoke_name
        # 模板替换变量
        self.sub_vars = sub_vars
