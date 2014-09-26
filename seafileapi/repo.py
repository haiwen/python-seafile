from seafileapi.utils import to_utf8

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
        repo_json = {k: to_utf8(v) for k, v in repo_json.iteritems()}

        repo_id = repo_json['id']
        repo_name = repo_json['name']
        repo_desc = repo_json['desc']
        encrypted = repo_json['encrypted']
        perm = repo_json['permission']
        owner = repo_json['owner']

        return cls(client, repo_id, repo_name, repo_desc, encrypted, owner, perm)

    def is_readonly(self):
        return 'w' not in self.perm

    def get_file(self, path):
        """Get the file object located in `path` in this library.

        Return a :class:`SeafFile` object
        """
        return SeafFile(self.client, self, path)

    def get_dir(self, path):
        """Get the dir object located in `path` in this library.

        Return a :class:`SeafDir` object
        """
        return SeafDir(self.client, self, path)

    def delete(self):
        self.client.delete('/api2/repos/' + self.id)
