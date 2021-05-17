

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
        pass

    def remove_member(self, username):
        pass

    def list_group_repos(self):
        pass
