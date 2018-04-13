import requests
from seafileapi.utils import urljoin
from seafileapi.exceptions import ClientHttpError
from seafileapi.repos import Repos

class SeafileApiClient(object):
    """Wraps seafile web api"""
    def __init__(self, server, username=None, password=None, token=None):
        """Wraps various basic operations to interact with seahub http api.
        """
        self.server = server
        self.username = username
        self.password = password
        self._token = token

        self.repos = Repos(self)
        self.groups = Groups(self)

        if token is None:
            self._get_token()

    def _get_token(self):
        data = {
            'username': self.username,
            'password': self.password,
        }
        url = urljoin(self.server, '/api2/auth-token/')
        res = requests.post(url, data=data)
        if res.status_code != 200:
            raise ClientHttpError(res.status_code, res.content)
        token = res.json()['token']
        assert len(token) == 40, 'The length of seahub api auth token should be 40'
        self._token = token

    def __str__(self):
        return 'SeafileApiClient[server=%s, user=%s]' % (self.server, self.username)

    __repr__ = __str__

    def get(self, *args, **kwargs):
        return self._send_request('GET', *args, **kwargs)

    def post(self, *args, **kwargs):
        return self._send_request('POST', *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self._send_request('delete', *args, **kwargs)

    def _send_request(self, method, url, *args, **kwargs):
        if not url.startswith('http'):
            url = urljoin(self.server, url)

        headers = kwargs.get('headers', {})
        headers.setdefault('Authorization', 'Token ' + self._token)
        kwargs['headers'] = headers

        expected = kwargs.pop('expected', 200)
        if not hasattr(expected, '__iter__'):
            expected = (expected, )

        resp = requests.request(method, url, *args, **kwargs)
        if resp.status_code not in expected:
            msg = 'Expected %s, but get %s' % \
                  (' or '.join(map(str, expected)), resp.status_code)
            msg += '\n' + resp.content.decode('utf-8')
            raise ClientHttpError(resp.status_code, msg)

        return resp


class Groups(object):
    def __init__(self, client):
        pass

    def create_group(self, name):
        pass
