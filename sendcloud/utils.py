from sendcloud.messsage import SendCloudEmailMessage


def sendcloud_template(to, tpt_ivk_name=None, sub_vars=None):
    """
    sub_vars: {}
    """
    mail = SendCloudEmailMessage(template_invoke_name=tpt_ivk_name,
                                 to=to, sub_vars=sub_vars)
    return mail.send()
