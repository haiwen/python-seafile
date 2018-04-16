from urllib import urlencode
from seafileapi.utils import utf8lize
from seafileapi.files import SeafDir, SeafFile
from seafileapi.utils import raise_does_not_exist
from seafileapi.exceptions import ClientHttpError, DoesNotExist


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

    @staticmethod
    def create_from_repo_id(client,repo_id):
        url = "/api2/repos/%s/"%(repo_id)
        resp = client.get(url).json()
        param = {
            "repo_name":resp["name"],
            "repo_desc":resp["desc"],
            "encrypted":resp["encrypted"],
            "owner":resp["owner"],
            "perm":resp["permission"]
        }
        return Repo(client, repo_id, **param)



    @classmethod
    def from_json(cls, client, repo_json):
        repo_json = utf8lize(repo_json)
        repo_id = repo_json['id']
        repo_name = repo_json['name']
        try:
            repo_desc = repo_json['desc']
        except:
            repo_desc = "No desc"
        encrypted = repo_json['encrypted']
        perm = repo_json['permission']
        owner = repo_json['owner']

        return cls(client, repo_id, repo_name, encrypted, owner, perm)

    def is_readonly(self):
        return 'w' not in self.perm

    def get_name(self):
        return self.name

    @raise_does_not_exist('The requested file does not exist')
    def get_file(self, path):
        """Get the file object located in `path` in this repo.

        Return a :class:`SeafFile` object
        """
        assert path.startswith('/')
        url = '/api2/repos/%s/file/detail/' % self.id
        query = '?' + urlencode(dict(p=path))
        file_json = self.client.get(url + query).json()

        return SeafFile(self.id, path, file_json['id'], file_json['size'],self.client)

    @raise_does_not_exist('The requested dir does not exist')
    def get_dir(self, path, recursive=True):
        """Get the dir object located in `path` in this repo.

        Return a :class:`SeafDir` object
        """
        assert path.startswith('/')
        url = '/api2/repos/%s/dir/' % self.id
        query = '?' + urlencode(dict(p=path))
        resp = self.client.get(url + query)
        dir_id = resp.headers['oid']
        dir_json = resp.json()
        dir = SeafDir(self.id, path, dir_id,0,self.client)

        if recursive:
            dir.load_entries(dir_json)
        return dir

    def is_exist_dir(self,path):
        '''
        Determine whether the path exists
        :param path:
        :return:
        '''
        exist = False
        try:
            dir = self.get_dir(path,False)
            if dir:
                exist = True
        except DoesNotExist:
            pass

        return exist



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
        if share_type == 'personal' and (users is None or len(users) == 0):
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
        params = dict(repo_name=self.name)
        self.client.post(url, data=params)

    def get_settings(self):
        """Get the settings of this repo. Returns a dict containing the following
        keys:

        `history_limit`: How many days of repo history to keep.
        """
        pass

    def restore(self, commit_id):
        pass

    def share_folder(self,path, share_type, users=None, group_id=None, permission=None):
        '''

        :param path:        [string]
        :param share_type:  [string] one of values: 'user', 'group' or 'public'.
        :param users:       [string] email
        :param group_id:    [int]
        :param permission:  [string] one of values: 'r' , 'rw'
        :return:
        '''
        return self._share_folder_operation('share',path, share_type=share_type, users=users, group_id=group_id, permission=permission)

    def unshare_folder(self,path, share_type, users=None, group_id=None, permission=None):
        '''

        :param path:        [string]
        :param share_type:  [string] one of values: 'user', 'group' or 'public'.
        :param users:       [string] email
        :param group_id:    [int]
        :param permission:  [string] one of values: 'r' , 'rw'
        :return:
        '''
        return self._share_folder_operation('unshare',path, share_type=share_type, users=users, group_id=group_id, permission=permission)

    def _share_folder_operation(self, operation, path, share_type, users=None, group_id=None, permission=None):
        """Manage sharing on this folder
        :param operation: Can be 'share' or 'unshare'
        :param share_type: Type of share, can be 'personal', 'group' or 'public'.
                           If personal, then users param must be specified.
                           If group, then group_id param must be specified.
       :param users: String, list or tuple of usernames/email addresses
       :param group_id: String group id from Seafile
       :param permission: String, 'r' or 'rw'
        """

        # /api2/repos/{repo-id}/dir/shared_items/?p={path}
        url = '/api2/repos/' + self.id + '/dir/shared_items/?' + urlencode(dict(p=path))

        if share_type not in ['user', 'group', 'public']:
            raise ValueError('Invalid share type: {}'.format(share_type))
        if share_type == 'personal' and users is None or len(users) == 0:
            raise ValueError('Invalid users supplied for personal share: {}'.format(users))
        if share_type == 'group' and group_id is None:
            raise ValueError('Invalid group_id for group share: {}'.format(group_id))
        if permission not in ['r', 'rw']:
            raise ValueError('Invalid permission: {}'.format(permission))

        if isinstance(users, (list, tuple)):
            users = ','.join(users)

        param =dict(share_type=share_type, username=users, group_id=group_id, permission=permission)
        # query = '?' + urlencode(dict(share_type=share_type, users=users, group_id=group_id, permission=permission))

        if operation == 'share':
            resp = self.client.put(url = url,data = param)
        elif operation == 'unshare':
            query = '&' + urlencode(param)
            resp = self.client.delete(url + query)
        else:
            raise ValueError('Invalid share operation: {}'.format(operation))

        return resp

class RepoRevision(object):
    def __init__(self, client, repo, commit_id):
        self.client = client
        self.repo = repo
        self.commit_id = commit_id

    def restore(self):
        """Restore the repo to this revision"""
        self.repo.revert(self.commit_id)
