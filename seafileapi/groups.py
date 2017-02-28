__author__ = 'commissar'

from seafileapi.group import AdminGroup,Group
from seafileapi.exceptions import GroupExisted,DoesNotExist

class Groups(object):
    def __init__(self, client):
        self.client = client

    def create_group(self, name):
        url = '/api/v2.1/groups/'
        params = dict(name=name)
        resp_str = self.client.post(url, data=params,expected=[400,200,201])
        if resp_str.status_code == 400:
            raise GroupExisted  #The group has existed!
        else:
            resp_json = resp_str.json()

        return resp_json


    def get_group(self,name):
        url = "/api2/groups/"
        resp_json = self.client.get(url).json()

        group = None
        groups = resp_json.get("groups",[])
        for grp in groups:
            if grp["name"] == name:
                group = Group(self.client, grp["id"], grp["name"])
                break

        return group


class AdminGroups(Groups):
    def __init__(self, client):
        super(AdminGroups,self).__init__(client)

    def list_groups(self):
        url = "/api/v2.1/admin/groups/?page=1&per_page=1000"
        resp_json = self.client.get(url).json()

        resp_groups = resp_json.get("groups",[])
        groups = []

        for item in resp_groups:
            grp = AdminGroup(self.client,group_id=item["id"],group_name=item["name"], owner=item["owner"])
            groups.append(grp)
        return groups


    def remove_group(self,group_name):
        grp_list = self.list_groups()

        for grp in grp_list:
            if grp.group_name == group_name:
                self._remove_group(grp.group_id)
                break



    def _remove_group(self, group_id):
        url = "/api/v2.1/admin/groups/%d/"%(group_id)
        self.client.delete(url)

