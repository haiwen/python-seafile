from seafileapi.utils import utf8lize


class Group(object):
    def __init__(self, client, group_id, group_name):
        self.client = client
        self.group_id = group_id
        self.group_name = group_name

    def list_members(self):
        url = "/api/v2.1/groups/%d/members/" % self.group_id
        resp_json = self.client.get(url, expected=[200]).json()
        members = []
        for member in resp_json:
            members.append(GroupMember.from_json(self.client, member))
        return members

    def delete(self):
        pass

    def add_member(self, username):
        url = "/api/v2.1/groups/%d/members/" % self.group_id
        params = { "email":username }
        resp_json = self.client.post(url, data=params,expected=[400,200,201]).json()
        return resp_json

    def set_member_admin(self,username):
        '''
        set member as admin for group
        :param username:
        :return:
        '''
        url = "/api/v2.1/groups/%d/members/%s/"%(self.group_id, username)
        params = { "is_admin":True }

        resp_json = self.client.put(url, data=params,expected=[200,201]).json()
        return resp_json

    def remove_member(self, username):
        url = "/api/v2.1/groups/%d/members/%s/" % (self.group_id, username)
        resp_json = self.client.delete(url, expected=[400,200,201]).json()
        return resp_json

    def list_group_repos(self):
        pass

    def transfer_group(self, owner):
        url = "/api/v2.1/groups/%s/"%self.group_id
        param = {owner:owner}
        resp_json = self.client.put(url,data=param).json()


class AdminGroup(object):
    def __init__(self, client, group_id, group_name,owner):
        self.client = client
        self.group_id = group_id
        self.group_name = group_name
        self.owner = owner


class GroupMember(object):
    def __init__(self, client, group_id, name, email, is_admin, role):
        self.client = client
        self.group_id = group_id
        self.name = name
        self.email = email
        self.is_admin = is_admin
        self.role = role

    @classmethod
    def from_json(cls, client, group_json):
        group_json = utf8lize(group_json)
        group_id = group_json['group_id']
        name = group_json['name']
        email = group_json['email']
        is_admin = group_json['is_admin']
        role = group_json['role']

        return cls(client, group_id, name, email, is_admin, role)
