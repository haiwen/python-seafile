import requests

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
        res = requests.post(TOKEN_URL, data=data)
        if res.status_code != 200:
            raise Exception(
        token = res.json()['token']
        return token

    def __str__(self):
