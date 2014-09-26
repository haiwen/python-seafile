from seafileapi.repo import Repo
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
