from seafileapi.account import Account


class SeafileAdmin(object):
    def __init__(self, client):
        self.client = client

    def lists_users(self, maxcount=100):
        pass

    def get_user(self, email):
        account_json = self.client.get('/api2/accounts/{}/'.format(email)).json()
        return Account.from_json(self.client, account_json)

    def list_user_repos(self, username):
        pass

    def is_exist_group(self,group_name):
        pass
