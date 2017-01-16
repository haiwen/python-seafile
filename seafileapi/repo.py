from urllib import urlencode
from seafileapi.utils import utf8lize
from seafileapi.files import SeafDir, SeafFile
from seafileapi.utils import raise_does_not_exist

class Repo(object):
    """
    A seafile library
    """
    def __init__(self, client, repo_id, repo_name, repo_desc,
                 encrypted, owner, perm):
        self.client = client
        self.id = repo_id
        self.name = repo_name
        self.desc = repo_desc
        self.encrypted = encrypted
        self.owner = owner
        self.perm = perm

    @classmethod
    def from_json(cls, client, repo_json):
        repo_json = utf8lize(repo_json)

        repo_id = repo_json['id']
        repo_name = repo_json['name']
        repo_desc = repo_json['desc']
        encrypted = repo_json['encrypted']
        perm = repo_json['permission']
        owner = repo_json['owner']

        return cls(client, repo_id, repo_name, repo_desc, encrypted, owner, perm)

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

    def _share_operation(self, operation, share_type, users=None, group_id=None, permission=None):
        """Manage sharing on this repo
        :param operation: Can be 'share' or 'unshare'
        :param share_type: Type of share, can be 'personal', 'group' or 'public'.
                           If personal, then users param must be specified.
                           If group, then group_id param must be specified.
       :param users: String, list or tuple of usernames/email addresses
       :param group_id: String group id from Seafile
       :param permission: String, 'r' or 'rw'
        """
        url = '/api2/shared-repos/' + self.id + '/'
        if share_type not in ['personal', 'group', 'public']:
            raise ValueError('Invalid share type: {}'.format(share_type))
        if share_type == 'personal' and users is None or len(users) == 0:
            raise ValueError('Invalid users supplied for personal share: {}'.format(users))
        if share_type == 'group' and group_id is None:
            raise ValueError('Invalid group_id for group share: {}'.format(group_id))
        if permission not in ['r', 'rw']:
            raise ValueError('Invalid permission: {}'.format(permission))
        if isinstance(users, (list, tuple)):
            users = ','.join(users)
        query = '?' + urlencode(dict(share_type=share_type, users=users, group_id=group_id, permission=permission))
        if operation == 'share':
            resp = self.client.put(url + query)
        elif operation == 'unshare':
            query = '?' + urlencode(dict(share_type=share_type, user=users, group_id=group_id, permission=permission))
            resp = self.client.delete(url + query)
        else:
            raise ValueError('Invalid share operation: {}'.format(operation))

    def share(self, share_type, users=None, group_id=None, permission=None):
        self._share_operation('share', share_type=share_type, users=users, group_id=group_id, permission=permission)

    def unshare(self, share_type, users=None, group_id=None, permission=None):
        if isinstance(users, (list, tuple)):
            # Unshare operation does not accept a list of users, only a single user
            raise TypeError('Unshare operation only accepts one user at a time')
        self._share_operation('unshare', share_type=share_type, users=users, group_id=group_id, permission=permission)

    ## Operations only the repo owner can do:

    def update(self):
        """Update the name and/or description of this repo. Only the repo owner can do
        this.
        """
        url = '/api2/repos/' + self.id + '/?op=rename'
        params = dict(repo_name=self.name, repo_desc=self.desc)
        self.client.post(url, data=params)

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
