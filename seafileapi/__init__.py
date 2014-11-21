from seafileapi.client import SeafileApiClient


def connect(server, username, password, **kwargs):
    client = SeafileApiClient(server, username, password, **kwargs)
    return client
