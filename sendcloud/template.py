#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from sendcloud import APIBaseClass


class SendCloudTemplate(APIBaseClass):

    def __init__(self, invoke_name, fail_silently=False, *args, **kwargs):
        _edm_user = kwargs.pop('edm_user', None)
        self.invoke_name = invoke_name
        try:
            self._edm_user = _edm_user or getattr(settings, 'MAIL_EDM_USER')
        except AttributeError:
            if fail_silently:
                self._edm_user = None
            else:
                raise

        self.get_url = 'http://sendcloud.sohu.com/webapi/template.get.json'
        self.add_url = 'http://sendcloud.sohu.com/webapi/template.add.json'
        self.update_url = 'http://sendcloud.sohu.com/webapi/template.update.json'
        self.send_url = 'http://sendcloud.sohu.com/webapi/mail.send_template.json'
        self.delete_url = 'http://sendcloud.sohu.com/webapi/template.delete.json'
        super(SendCloudTemplate, self).__init__(*args, **kwargs)

    @property
    def edm_user(self):
        return self._edm_user

    def get_or_create(self, **kwargs):
        if not self.get_status():
            self.add(**kwargs)

    def update_or_create(self, **kwargs):
        if not self.get_status():
            self.add(**kwargs)
        else:
            self.update(**kwargs)

    def get_status(self):
        data = {
            'api_user': self.api_user,
            'api_key': self.api_key,
            'invoke_name': self.invoke_name
        }

        res = self.post_api(self.get_url, data)

        if len(res['templateList']) == 0:
            return False
        try:
            template_info = res['templateList'][0]
            return template_info['is_verify']
        except Exception:
            if not self.fail_silently:
                raise
            return False

    def add(self, name, html, subject, email_type=1):
        data = {
            'api_user': self.api_user,
            'api_key': self.api_key,
            'invoke_name': self.invoke_name,
            'name': name,
            'html': html,
            'subject': subject,
            'email_type': email_type
        }
        return self.post_api(self.add_url, data)

    def update(self, name, html, subject, email_type=1):
        data = {
            'api_user': self.api_user,
            'api_key': self.api_key,
            'invoke_name': self.invoke_name,
            'name': name,
            'html': html,
            'subject': subject,
            'email_type': email_type
        }
        return self.post_api(self.update_url, data)

    def delete(self):
        data = {
            'api_user': self.api_user,
            'api_key': self.api_key,
            'invoke_name': self.invoke_name,
        }
        res = self.post_api(self.delete_url, data)
        return res

    def send_to_list(self, subject, from_mail, from_name, to):
        data = {
            'api_user': self.edm_user,
            'api_key': self.api_key,
            'use_maillist': 'true',
            'resp_email_id': 'true',
            'template_invoke_name': self.invoke_name,
            'subject': subject,
            'to': to,
            "from": from_mail,
            "mail_from": from_mail,
            "fromname": from_name,
        }
        return self.post_api(self.send_url, data)
