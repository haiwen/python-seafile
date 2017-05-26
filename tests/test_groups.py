__author__ = 'commissar'

import pytest

from seafileapi.groups import Groups,AdminGroups

@pytest.fixture(scope='function')
def groups(client):
    return Groups(client)

def test_create_group(client,groups):
    grp_mgr = Groups(client)

    resp= grp_mgr.create_group("黄河s火车")
    print(resp)

def test_add_admin_to_group(client,groups):
    grp_boj = groups.get_group("黄河s火车")

    new_memeber_email = "1051708338@qq.com"
    grp_boj.add_member(new_memeber_email)
    grp_boj.set_member_amdin(new_memeber_email)

    print(grp_boj)

def test_admin_remove_group(client):

    admin_grp_mgr = AdminGroups(client)

    grp_list = admin_grp_mgr.list_groups()

    for grp in grp_list:
        if grp.group_name == "黄河s火车":
            admin_grp_mgr.remove_group("黄河s火车")



def test_admin_list_groups(client):
    admin_grp_mgr = AdminGroups(client)

    grp_list = admin_grp_mgr.list_groups()

    print(grp_list)