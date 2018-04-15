
class Groups(object):
    def __init__(self, client):
        """
        client -- Seafile client object
        """
        self.client = client

    def get_groups(self):
        """
        Returns list of groups
        """
        resp = self.client.get('/api2/groups/')
        value = resp.json()
        return value['groups']

#     def get_group_members(self, group_name):
#         """
#         Returns list of members of a group
#         """
#         groups = self.get_groups()
#         found = False
#         for i in groups:
#             if i['name'] == group_name:
#                 url = '/api2/groups/{}/members/'.format(i['id'])
#                 resp = self.client.get(url)
#                 found = True
#                 break
#         value = resp.json()
#         return value

    def create_group(self, group_name):
        """
        Creates group

        group_name -- name
        """
        data = {
            'group_name': group_name,
        }
        resp = self.client.put(
            '/api2/groups/',
            data=data,
        )
        value = resp.json()
        return value

    def delete_group(self, group_name):
        """
        Delete group

        group_name -- name
        """
        url = '/api2/groups/{}'.format(self.get_id_from_group_name(group_name))
        resp = self.client.delete(url)
        value = resp.json()
        return value

    def get_id_from_group_name(self, group_name):
        groups = self.get_groups()
        for i in groups:
            if i['name'] == group_name:
                return i['id']

        raise ValueError('Group {} not found'.format(group_name))


# class Group(object):
#     def __init__(self, client, group_id, group_name):
#         self.client = client
#         self.group_id = group_id
#         self.group_name = group_name
# 
#     def list_memebers(self):
#         pass
# 
#     def delete(self):
#         pass
# 
#     def add_member(self, username):
#         pass
# 
#     def remove_member(self, username):
#         pass
# 
#     def list_group_repos(self):
#         pass
