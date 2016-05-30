import json

import requests
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import sanitize_address


class SendCloudAPIError(Exception):
    pass


class SendCloudBackend(BaseEmailBackend):
    """
        A Django Email backend that uses send cloud.
    """

    def __init__(self, fail_silently=False, *args, **kwargs):
        app_user, app_key = (kwargs.pop('app_user', None),
                             kwargs.pop('app_key', None))

        super(SendCloudBackend, self).__init__(fail_silently=fail_silently,
                                               **kwargs)
        try:
            self._app_user = app_user or getattr(settings, 'MAIL_APP_USER')
            self._app_key = app_key or getattr(settings, 'MAIL_APP_KEY')
        except AttributeError:
            if fail_silently:
                self._app_user, self._app_key = None, None
            else:
                raise
        # print self._app_key, self._app_user
        self._api_url = "http://sendcloud.sohu.com/webapi/mail.send_template.json"

    @property
    def app_user(self):
        return self._app_user

    @property
    def app_key(self):
        return self._app_key

    @property
    def api_url(self):
        return self._api_url

    def open(self):
        pass

    def close(self):
        pass

    def _send(self, email_message):
        """A helper method that does the actual sending."""
        if not email_message.recipients():
            return False
        if settings.MAIL_DEBUG:
            return True
        from_name = sanitize_address(email_message.from_email,
                                     email_message.encoding)
        recipients = [sanitize_address(addr, email_message.encoding)
                      for addr in email_message.recipients()]

        sub_vars = {
            'to': recipients,
            'sub': json.dumps(email_message.sub_vars)
        }

        params = {
            "api_user": self.app_user,
            "api_key": self.app_key,
            "template_invoke_name": email_message.template_invoke_name,
            "substitution_vars": json.dumps(sub_vars),
            "from": settings.DEFAULT_FROM_EMAIL,
            "fromname": from_name,
            "resp_email_id": "true",
        }

        try:
            r = requests.post(self.api_url, data=params)
        except Exception:
            if not self.fail_silently:
                raise
            return False
        res = r.json()
        if 'errors' in res:
            if not self.fail_silently:
                raise SendCloudAPIError(res['errors'])
            return False

        return True

    def send_messages(self, email_messages):
        """Sends one or more EmailMessage objects and returns the number of
        email messages sent.
        """
        if not email_messages:
            return

        num_sent = 0
        for message in email_messages:
            if self._send(message):
                num_sent += 1
        return num_sent


class APIBaseClass(object):
    def __init__(self, fail_silently=False, *args, **kwargs):
        api_user, api_key = (kwargs.pop('app_user', None),
                             kwargs.pop('app_key', None))
        self.fail_silently = fail_silently
        try:
            self._api_user = api_key or getattr(settings, 'MAIL_APP_USER')
            self._api_key = api_key or getattr(settings, 'MAIL_APP_KEY')
        except AttributeError:
            if fail_silently:
                self._api_user, self._api_key = None, None
            else:
                raise

    @property
    def api_user(self):
        return self._api_user

    @property
    def api_key(self):
        return self._api_key

    def post_api(self, url, data):
        try:
            r = requests.post(url, data=data)
        except Exception:
            if not self.fail_silently:
                raise
            return False

        res = r.json()

        if 'errors' in res:
            if not self.fail_silently:
                raise SendCloudAPIError(res['errors'])
            return False

        return res
