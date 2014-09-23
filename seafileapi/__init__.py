from seafileapi.client import SeafileApiClient

def connect(server, username, password):
    client = SeafileApiClient(server, username, password)
    return client
