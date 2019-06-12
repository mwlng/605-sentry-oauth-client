# -*- coding: utf-8 -*-

"""
605 Sentry client class
"""

import re
import requests

from bs4 import BeautifulSoup


class SentryClient(object):

    def __init__(self, server_url, client_id, auth_url, redirect_url, scopes=['public'], state='xyz'):
        self._oauth_server = server_url
        self._oauth_client_id = client_id
        self._oauth_authorization_url = auth_url
        self._oauth_redirect_uri = redirect_url
        self._oauth_scopes = scopes
        self._oauth_state = state

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        pass

    def _extract_authenticity_token(self, input):
        soup = BeautifulSoup(input, 'html.parser')
        return soup.body.form.find(attrs={'name': 'authenticity_token'}).attrs['value']

    def get_access_token(self, username, password, signin_uri='/users/sign_in'):
        sess = requests.session()
        resp = sess.get(self._oauth_server)
        authenticity_token = self._extract_authenticity_token(resp.content)
        payload = {
            'authenticity_token': authenticity_token,
            'user[email]': username,
            'user[password]': password,
            'user[remember_me]': 0,
            'commit': 'Login'
        }

        resp = sess.post(url=self._oauth_server + signin_uri, data=payload)
        params = {
            'client_id': self._oauth_client_id,
            'response_type': 'token',
            'scopes': self._oauth_scopes,
            'redirect_uri': self._oauth_redirect_uri,
            'state': self._oauth_state
        }
        resp = sess.get(self._oauth_authorization_url, params=params)
        pattern = r"%s#access_token=(.*)&token_type=bearer&expires_in=900&state=xyz" % self._oauth_redirect_uri
        m = re.match(pattern, resp.url)
        return m.group(1)
