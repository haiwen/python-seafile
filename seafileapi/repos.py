from seafileapi.repo import Repo,SharedFolder
from seafileapi.utils import raise_does_not_exist

class Repos(object):
    def __init__(self, client):
        self.client = client

    def create_repo(self, name, desc, password=None):
        data = {'name': name, 'desc': desc}
        if password:
            data['passwd'] = password
        repo_json = self.client.post('/api2/repos/', data=data).json()
        return self.get_repo(repo_json['repo_id'])

    @raise_does_not_exist('The requested library does not exist')
    def get_repo(self, repo_id):
        """Get the repo which has the id `repo_id`.

        Raises :exc:`DoesNotExist` if no such repo exists.
        """
        repo_json = self.client.get('/api2/repos/' + repo_id).json()
        return Repo.from_json(self.client, repo_json)

    def list_repos(self):
        repos_json = self.client.get('/api2/repos/').json()
        return  [Repo.from_json(self.client, j) for j in repos_json]

    def list_shared_folders(self,shared_email=None):
        '''
        List Shared Folders
        :param  shared_email    [string|None]According to the email to filter on the Shared folder. if None then no filter.
        :return:    [list(SharedFolder)]
        '''

        repos_json = self.client.get('/api/v2.1/shared-folders/').json()
        shared_folders = []

        for t_folder in repos_json:

            folder_obj = SharedFolder(self.client, **t_folder)
            t_user_email = folder_obj.get("user_email",None)

            if shared_email:
                if t_user_email == shared_email:
                    shared_folders.append(t_folder)
            else:
                shared_folders.append(t_folder)

        return repos_json




