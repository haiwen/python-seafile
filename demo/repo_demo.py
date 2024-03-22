from seafileapi import SeafileAPI, Repo



server_url = "http://127.0.0.1:8000/"
login_name = "example@examle.com"
pwd = "password"

api_token = '6de40d8456b06bdb4c9eabbf658175bdc4084050'


seafile_api = SeafileAPI(login_name, pwd, server_url)
seafile_api.auth()


user_repo = seafile_api.get_repo('2ce3ec78-d347-412c-b157-fce3c0d30ebb')

api_repo = Repo(api_token, server_url)
api_repo.auth()

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

print(user_repo.rename_file('/d','d2'))
print(api_repo.rename_file('','f2'))

# print(user_repo.delete_file(''))
# print(api_repo.delete_file('/'))