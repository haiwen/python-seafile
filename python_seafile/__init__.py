from python_seafile.client import SeafileApiClient
from python_seafile._version import __version__

def connect(server, username, password):
    client = SeafileApiClient(server, username, password)
    return client
