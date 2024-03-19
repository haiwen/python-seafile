from seafileapi import SeafileAPI, Repo


# server_url = "https://cloud.seafile.com"
# login_name = "example@seafile.com"
# pwd = "xxxx"
#
# api_token = '8d2d8dbace764decc58e9ea47d027f7ca2a9aa27'

server_url = "http://127.0.0.1:8000/"
login_name = "350178982_tmp@qq.com"
pwd = "111"

api_token = '6de40d8456b06bdb4c9eabbf658175bdc4084050'


seafile_api = SeafileAPI(login_name, pwd, server_url)
seafile_api.auth()


user_repo = seafile_api.get_repo('fedd5bc8-3da3-4be3-91d4-00b90c7de77f')

api_repo = Repo(api_token, server_url)
api_repo.auth()



print(user_repo.get_repo_details())
print(api_repo.get_repo_details())

# print(user_repo.list_dir('/seafile-api/共享'))
# print(api_repo.list_dir('/images'))