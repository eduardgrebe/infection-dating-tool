from api import api
from django.conf import settings
import requests
from importlib import import_module
SessionStore = import_module(settings.SESSION_ENGINE).SessionStore

class ApiSession(object):
    def __init__(self, username, password, ui_login=True):
        response = api.post_with_token(None, "users/login", { 
            'username': username,
            'password': password 
        })

        if response['status'] == 'ok':
            self._token = response['api_token']
            self._user = response['user']

            if ui_login:
                session = requests.Session()
                session.get(settings.BASE_URL + settings.LOGIN_URL)
                post_data = {
                    'username': username, 
                    'password': password,
                    'csrfmiddlewaretoken': session.cookies['csrftoken']
                }
                session.post(settings.BASE_URL + settings.LOGIN_URL, data=post_data)
                self._session = session
                self._token = SessionStore(session.cookies['sessionid'])['api_token']
                self.session = {'api_token': self._token}

    def post(self, *args, **kwargs):
        return api.post_with_token(self._token, *args, **kwargs)

    def get(self, *args, **kwargs):
        return api.get_with_token(self._token, *args, **kwargs)

    def ui_get(self, url, *args, **kwargs):
        if not (url.startswith('http://') or url.startswith('https://')):
            if not url.startswith('/'):
                url = '/' + url
            url = settings.BASE_URL + url
        return self._session.get(url, *args, **kwargs)

    def ui_post(self, url, *args, **kwargs):
        if not (url.startswith('http://') or url.startswith('https://')):
            if not url.startswith('/'):
                url = '/' + url
            url = settings.BASE_URL + url
        return self._session.post(url, *args, **kwargs)
    

