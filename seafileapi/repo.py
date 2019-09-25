from urllib.parse import urlencode
from seafileapi.utils import utf8lize
from seafileapi.files import SeafDir, SeafFile
from seafileapi.utils import raise_does_not_exist

class Repo(object):
    """
    A seafile library
    """
    def __init__(self, client, repo_id, repo_name,
                 encrypted, owner, perm):
        self.client = client
        self.id = repo_id
        self.name = repo_name
        self.encrypted = encrypted
        self.owner = owner
        self.perm = perm

    @classmethod
    def from_json(cls, client, repo_json):
        repo_json = utf8lize(repo_json)

        repo_id = repo_json['id']
        repo_name = repo_json['name']
        encrypted = repo_json['encrypted']
        perm = repo_json['permission']
        owner = repo_json['owner']

        return cls(client, repo_id, repo_name, encrypted, owner, perm)

    def is_readonly(self):
        return 'w' not in self.perm

    @raise_does_not_exist('The requested file does not exist')
    def get_file(self, path):
        """Get the file object located in `path` in this repo.

        Return a :class:`SeafFile` object
        """
        assert path.startswith('/')
        url = '/api2/repos/%s/file/detail/' % self.id
        query = '?' + urlencode(dict(p=path))
        file_json = self.client.get(url + query).json()

        return SeafFile(self, path, file_json['id'], file_json['size'])

    @raise_does_not_exist('The requested dir does not exist')
    def get_dir(self, path):
        """Get the dir object located in `path` in this repo.

        Return a :class:`SeafDir` object
        """
        assert path.startswith('/')
        url = '/api2/repos/%s/dir/' % self.id
        query = '?' + urlencode(dict(p=path))
        resp = self.client.get(url + query)
        dir_id = resp.headers['oid']
        dir_json = resp.json()
        dir = SeafDir(self, path, dir_id)
        dir.load_entries(dir_json)
        return dir

    def delete(self):
        """Remove this repo. Only the repo owner can do this"""
        self.client.delete('/api2/repos/' + self.id)

    def list_history(self):
        """List the history of this repo

        Returns a list of :class:`RepoRevision` object.
        """
        pass

    ## Operations only the repo owner can do:

    def update(self, name=None):
        """Update the name of this repo. Only the repo owner can do
        this.
        """
        pass

    def get_settings(self):
        """Get the settings of this repo. Returns a dict containing the following
        keys:

        `history_limit`: How many days of repo history to keep.
        """
        pass

    def restore(self, commit_id):
        pass

class RepoRevision(object):
    def __init__(self, client, repo, commit_id):
        self.client = client
        self.repo = repo
        self.commit_id = commit_id

    def restore(self):
        """Restore the repo to this revision"""
        self.repo.revert(self.commit_id)
