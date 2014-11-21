from seafileapi.client import SeafileApiClient


def connect(server, username, password, request_kwargs=None):
    client = SeafileApiClient(server, username, password, request_kwargs)
    return client
