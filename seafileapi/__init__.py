from seafileapi.client import SeafileApiClient
from setup.py import __version__

def connect(server, username, password):
    client = SeafileApiClient(server, username, password)
    return client
