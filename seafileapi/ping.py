class Ping(object):
    def __init__(self, client):
        self.client = client

    def auth_ping(self):
        """Call the authenticated 'ping' endpoint. Useful to test credential validity."""
        response = self.client.get('/api2/auth/ping/').content
        print response