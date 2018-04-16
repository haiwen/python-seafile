from seafileapi.account import Account
from seafileapi.exceptions import UserExisted, DoesNotExist


class SeafileAdmin(object):
    def __init__(self, client):
        self.client = client

    def lists_users(self, maxcount=100):
        pass

    def get_user(self, email):
        account_json = self.client.get('/api2/accounts/{}/'.format(email)).json()
        return Account.from_json(self.client, account_json)

    def create_user(self, email, password, is_active=True, is_staff=False):
        url = '/api2/accounts/{}/'.format(email)
        params = {'password': password,
                  'is_active': is_active and 'true' or 'false',
                  'is_staff': is_staff and 'true' or 'false'}
        result = self.client.put(url, data=params, expected=[200, 201])
        if result.status_code == 201:
            return result.json()  # User created
        elif result.status_code == 200:
            raise UserExisted()

    def delete(self, email):
        url = '/api2/accounts/{}/'.format(email)
        result = self.client.delete(url, expected=[200, 202])
        if result.status_code == 200:
            return True
        elif result.status_code == 202:
            raise DoesNotExist('User {}'.format(email))

    def list_user_repos(self, username):
        pass

    def is_exist_group(self,group_name):
        pass
