import requests
from seafileapi.utils import urljoin
from seafileapi.exceptions import ClientHttpError
from seafileapi.repos import Repos

class SeafileApiClient(object):
    """Wraps seafile web api"""
    def __init__(self, server, username, password, request_kwargs=None):
        """Wraps various basic operations to interact with seahub http api.
        """
        self.server = server
        self.username = username
        self.password = password
        # FIXME: filter valid kwargs
        self.request_kwargs = request_kwargs or {}
        self._token = None

        self.repos = Repos(self)
        self.groups = Groups(self)

        self._get_token()

    def _get_token(self):
        data = {
            'username': self.username,
            'password': self.password,
        }
        url = urljoin(self.server, '/api2/auth-token/')
        res = requests.post(url, data=data, **self.request_kwargs)
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
        keyword_args = self.request_kwargs.copy()
        keyword_args.update(kwargs)
        
        if not url.startswith('http'):
            url = urljoin(self.server, url)

        headers = keyword_args.get('headers', {})
        headers.setdefault('Authorization', 'Token ' + self._token)
        keyword_args['headers'] = headers

        expected = keyword_args.pop('expected', 200)
        if not hasattr(expected, '__iter__'):
            expected = (expected, )
        resp = requests.request(method, url, *args, **keyword_args)
        if resp.status_code not in expected:
            msg = 'Expected %s, but get %s' % \
                  (' or '.join(map(str, expected)), resp.status_code)
            raise ClientHttpError(resp.status_code, msg)

        return resp


class Groups(object):
    def __init__(self, client):
        pass

    def create_group(self, name):
        pass
