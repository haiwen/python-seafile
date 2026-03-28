import sys
sys.path.append('..')

from seafileapi import SeafileAPI, Repo
from configparser import ConfigParser


config = ConfigParser()
config.read('test.ini')

server_url = config.get('account', 'server_url')
login_name = config.get('account', 'login_name')
pwd = config.get('account', 'password')
account_token = config.get('account', 'account_token')
test_uuid = config.get('account', 'test_repo_uuid')

repo_token = config.get('repo', 'repo_token')


# Auth with password
print('Auth with password...')
seafile_api_pwd = SeafileAPI(login_name, pwd, server_url)
seafile_api_pwd.auth()
user_repo_pwd = seafile_api_pwd.get_repo(test_uuid)
print(user_repo_pwd.list_dir())

# Auth with account_token
print('Auth with account_token...')
seafile_api_token = SeafileAPI.from_auth_token(account_token, server_url)
seafile_api_token.auth()
user_repo_token = seafile_api_token.get_repo(test_uuid)
print(user_repo_token.list_dir())

# Using repo_token
print('Using repo_token...')
api_repo = Repo(repo_token, server_url)
api_repo.auth()
print(api_repo.list_dir())



'''seafileAPI'''
# print(seafile_api.list_repos())
# print(seafile_api.get_repo('d5620899-1e9b-4a8c-b9af-b00a26324407'))
# print(seafile_api.create_repo('tttt'))
# print(seafile_api.delete_repo('9600ba12-4ac0-43da-b5ee-7aed7cdfcc58'))


# print(user_repo.get_repo_details())
# print(api_repo.get_repo_details())

# print(user_repo.list_dir('/'))
# print(api_repo.list_dir('/'))

# print(user_repo.create_dir(p='/123',create_parents=True))
# print(api_repo.create_dir(p='/222'))

# print(user_repo.rename_dir(p='/1',newname='python1'))
# print(api_repo.rename_dir(p='/2',newname='python2'))

# print(user_repo.delete_dir("/1"))
# print(api_repo.delete_dir("/2"))

# print(user_repo.get_file("/q"))
# print(api_repo.get_file("/q"))

# print(user_repo.create_file(""))
# print(api_repo.create_file("q"))

# print(user_repo.rename_file('/d','d2'))
# print(api_repo.rename_file('','f2'))

# print(user_repo.delete_file(''))
# print(api_repo.delete_file('/'))