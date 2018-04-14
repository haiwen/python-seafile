from group import Group


class User(object):
    def __init__(self, client):
        """
        client -- Seafile client object
        """
        self.client = client

    def get_accounts(self):
        """
        Returns accounts list such as :

        [{'source': 'DB', 'email': 'test@seafiletest.com'},
        {'source': 'DB', 'email': 'admin@seafiletest.com'}]
        """
        url = '/api2/accounts/'
        resp = self.client.get(url)
        return resp.json()

    def create_account(self, email, password, groups_names=[], name='', note='', is_staff=False, is_active=True):
        """
        Creates account

        email -- email as login name
        password -- plain text password
        name -- full text display name
        groups_names -- list of groups' names to add this user to
        note -- description / comment / whatever
        is_staff -- is admin, default False
        is_active -- can connect, default True
        """
        data = {
            'password': password,
            'is_staff': is_staff,
            'is_active': is_active,
            'name': name[0:64],
            'note': note,
            # 'storage': 'DB',
        }
        url = '/api2/accounts/{}/'.format(email)
        resp = self.client.put(
            url,
            data=data,
            expected=[200, 201],
        )
        user = resp.json()
        for group_name in groups_names:
            self.add_user_to_group(username=email, group_name=group_name)

        return user

    def delete_account(self, email):
        """
        Delete account

        email -- email as login name
        """
        url = '/api2/accounts/{}/'.format(email)
        resp = self.client.delete(url)
        value = resp.json()
        return value

    def add_user_to_group(self, username, group_name):
        """
        Adds given username (email) to group (by group name)

        username -- email / login name
        group_name -- group to add user to
        """
        data = {
            'user_name': username,
        }
        url = '/api2/groups/{}/members/'.format(self.__get_id_from_group_name__(group_name))
        resp = self.client.put(
            url, data=data,
        )

        return resp.json()

    def __get_groups__(self):
        manage_group = Group(self.client)
        return manage_group.get_groups()

    def __get_id_from_group_name__(self, group_name):
        manage_group = Group(self.client)
        return manage_group.get_id_from_group_name(group_name)

        
    
"""
import __init__
c=__init__.connect('http://127.0.0.1:8000', 'admin@seafiletest.com', 'adminadmin')
from user import User
u=User(c)
u.create_account('none5@xael.org', 'node99', ['test'], 'Alexandre')
# u.delete_group('TEST2')
# u.delete_account('none4@xael.org')
u.get_group_members('test')
"""
