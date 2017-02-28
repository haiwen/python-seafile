

class Group(object):
    def __init__(self, client, group_id, group_name):
        self.client = client
        self.group_id = group_id
        self.group_name = group_name

    def list_memebers(self):
        pass

    def delete(self):
        pass

    def add_member(self, username):
        url = "/api/v2.1/groups/%d/members/"%self.group_id
        params = { "email":username }
        resp_json = self.client.post(url, data=params,expected=[400,200,201]).json()
        return resp_json

    def set_member_amdin(self,username):
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
        pass

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


