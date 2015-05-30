import io
import os
import posixpath
import re
from seafileapi.utils import querystr, utf8lize

ZERO_OBJ_ID = '0000000000000000000000000000000000000000'

class _SeafDirentBase(object):
    """Base class for :class:`SeafFile` and :class:`SeafDir`.

    It provides implementation of their common operations.
    """
    isdir = None

    def __init__(self, repo, path, object_id, size=0):
        """
        :param:`path` the full path of this entry within its repo, like
        "/documents/example.md"

        :param:`size` The size of a file. It should be zero for a dir.
        """
        self.client = repo.client
        self.repo = repo
        self.path = path
        self.id = object_id
        self.size = size

    @property
    def name(self):
        return posixpath.basename(self.path)

    def list_revisions(self):
        pass

    def delete(self):
        suffix = 'dir' if self.isdir else 'file'
        url = '/api2/repos/%s/%s/' % (self.repo.id, suffix) + querystr(p=self.path)
        resp = self.client.delete(url)
        return resp

    def rename(self, newname):
        """Change filename to newname
        """
        url = '/api2/repos/%s/file/' % self.repo.id + querystr(p=self.path)
        postdata = {'operation': 'rename', 'newname': newname}
        resp = self.client.post(url, data=postdata)
        self.id = resp.headers['oid']

    def copyTo(self, file_names, dst_dir, dst_repo=None):
        """Copy filename to newname (also to a different directory)
        """
        src_dir = os.path.dirname(self.path)
        url = '/api2/repos/%s/fileops/copy/' % self.repo.id + querystr(p=src_dir)
        if dst_repo is None:
            dst_repo = self.repo.id
        postdata = {'operation': 'copy', 'file_names': file_names, 'dst_repo': dst_repo, 'dst_dir': dst_dir}
        resp = self.client.post(url, data=postdata)
        self.id = resp.headers['oid']

    def moveTo(self, dst_dir, dst_repo=None):
        """Move filename to newname (also to a different directory)
        """
        url = '/api2/repos/%s/file/' % self.repo.id + querystr(p=self.path)
        if dst_repo is None:
            dst_repo = self.repo.id
        postdata = {'operation': 'move', 'dst_repo': dst_repo, 'dst_dir': dst_dir}
        resp = self.client.post(url, data=postdata)
        self.id = resp.headers['oid']

    def get_share_link(self):
        pass

class SeafDir(_SeafDirentBase):
    isdir = True

    def __init__(self, *args, **kwargs):
        super(SeafDir, self).__init__(*args, **kwargs)
        self.entries = None
        self.entries = kwargs.pop('entries', None)

    def ls(self, force_refresh=False):
        """List the entries in this dir.

        Return a list of objects of class :class:`SeafFile` or :class:`SeafDir`.
        """
        if self.entries is None or force_refresh:
            self.load_entries()

        return self.entries

    def create_empty_file(self, name):
        """Create a new empty file in this dir.
        Return a :class:`SeafFile` object of the newly created file.
        """
        # TODO: file name validation
        path = posixpath.join(self.path, name)
        url = '/api2/repos/%s/file/' % self.repo.id + querystr(p=path, reloaddir='true')
        postdata = {'operation': 'create'}
        resp = self.client.post(url, data=postdata)
        self.id = resp.headers['oid']
        self.load_entries(resp.json())
        return SeafFile(self.repo, path, ZERO_OBJ_ID, 0)

    def mkdir(self, name):
        """Create a new sub folder right under this dir.

        Return a :class:`SeafDir` object of the newly created sub folder.
        """
        path = posixpath.join(self.path, name)
        url = '/api2/repos/%s/dir/' % self.repo.id + querystr(p=path, reloaddir='true')
        postdata = {'operation': 'mkdir'}
        resp = self.client.post(url, data=postdata)
        self.id = resp.headers['oid']
        self.load_entries(resp.json())
        return SeafDir(self.repo, path, ZERO_OBJ_ID)

    def upload(self, fileobj, filename):
        """Upload a file to this folder.

        :param:fileobj :class:`File` like object
        :param:filename The name of the file

        Return a :class:`SeafFile` object of the newly uploaded file.
        """
        if isinstance(fileobj, str):
            fileobj = io.BytesIO(fileobj)
        upload_url = self._get_upload_link()
        files = {
            'file': (filename, fileobj),
            'parent_dir': self.path,
        }
        self.client.post(upload_url, files=files)
        return self.repo.get_file(posixpath.join(self.path, filename))

    def upload_local_file(self, filepath, name=None):
        """Upload a file to this folder.

        :param:filepath The path to the local file
        :param:name The name of this new file. If None, the name of the local file would be used.

        Return a :class:`SeafFile` object of the newly uploaded file.
        """
        name = name or os.path.basename(filepath)
        with open(filepath, 'r') as fp:
            return self.upload(fp, name)

    def _get_upload_link(self):
        url = '/api2/repos/%s/upload-link/' % self.repo.id
        resp = self.client.get(url)
        return re.match(r'"(.*)"', resp.text).group(1)

    def get_uploadable_sharelink(self):
        """Generate a uploadable shared link to this dir.

        Return the url of this link.
        """
        pass

    def load_entries(self, dirents_json=None):
        if dirents_json is None:
            url = '/api2/repos/%s/dir/' % self.repo.id + querystr(p=self.path)
            dirents_json = self.client.get(url).json()

        self.entries = [self._load_dirent(entry_json) for entry_json in dirents_json]

    def _load_dirent(self, dirent_json):
        dirent_json = utf8lize(dirent_json)
        path = posixpath.join(self.path, dirent_json['name'])
        if dirent_json['type'] == 'file':
            return SeafFile(self.repo, path, dirent_json['id'], dirent_json['size'])
        else:
            return SeafDir(self.repo, path, dirent_json['id'], 0)

    @property
    def num_entries(self):
        if self.entries is None:
            self.load_entries()
        return len(self.entries) if self.entries is not None else 0
    
    def __str__(self):
        return 'SeafDir[repo=%s,path=%s,entries=%s]' % \
            (self.repo.id[:6], self.path, self.num_entries)

    __repr__ = __str__

class SeafFile(_SeafDirentBase):
    isdir = False
    def update(self, fileobj):
        """Update the content of this file"""
        pass

    def __str__(self):
        return 'SeafFile[repo=%s,path=%s,size=%s]' % \
            (self.repo.id[:6], self.path, self.size)

    def _get_download_link(self):
        url = '/api2/repos/%s/file/' % self.repo.id + querystr(p=self.path)
        resp = self.client.get(url)
        return re.match(r'"(.*)"', resp.text).group(1)

    def get_content(self):
        """Get the content of the file"""
        url = self._get_download_link()
        return self.client.get(url).content

    __repr__ = __str__
