import requests
from seafileapi.utils import urljoin

class ClientHttpError(Exception):
    """This exception is raised if the returned http response is not as
    expected"""
    def __init__(self, code, message):
        super(ClientHttpError, self).__init__(code, message)

    def __str__(self):
        return 'ClientHttpError[%s: %s]' % (self.code, self.message)

class SeafileApiClient(object):
    """Wraps seafile web api"""
    def __init__(self, server, username, password):
        """
        """
        self.server = server
        self.username = username
        self.password = password
        self._token = None
        self._get_token()

    def _get_token(self):
        data = {
            'username': self.username,
            'password': self.password,
        }
        url = urljoin(self.server, '/api2/auth-token/')
        res = requests.post(url, data=data)
        if res.status_code != 200:
            raise ClientHttpError(res.status_code, res.data)
        token = res.json()['token']
        return token

    def __str__(self):
        return 'SeafileApiClient[server=%s, user=%s]' % (self.server, self.username)
