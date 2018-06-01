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
        """Change file/folder name to newname
        """
        suffix = 'dir' if self.isdir else 'file'
        url = '/api2/repos/%s/%s/' % (self.repo.id, suffix) + querystr(p=self.path, reloaddir='true')
        postdata = {'operation': 'rename', 'newname': newname}
        resp = self.client.post(url, data=postdata)
        succeeded = resp.status_code == 200
        if succeeded:
            if self.isdir:
                new_dirent = self.repo.get_dir(os.path.join(os.path.dirname(self.path), newname))
            else:
                new_dirent = self.repo.get_file(os.path.join(os.path.dirname(self.path), newname))
            for key in self.__dict__.keys():
                self.__dict__[key] = new_dirent.__dict__[key]
        return succeeded

    def _copy_move_task(self, operation, dirent_type, dst_dir, dst_repo_id=None):
        url = '/api/v2.1/copy-move-task/'
        src_repo_id = self.repo.id
        src_parent_dir = os.path.dirname(self.path)
        src_dirent_name = os.path.basename(self.path)
        dst_repo_id = dst_repo_id
        dst_parent_dir = dst_dir
        operation = operation
        dirent_type =  dirent_type
        postdata = {'src_repo_id': src_repo_id, 'src_parent_dir': src_parent_dir,
                    'src_dirent_name': src_dirent_name, 'dst_repo_id': dst_repo_id,
                    'dst_parent_dir': dst_parent_dir, 'operation': operation,
                    'dirent_type': dirent_type}
        return self.client.post(url, data=postdata)

    def copyTo(self, dst_dir, dst_repo_id=None):
        """Copy file/folder to other directory (also to a different repo)
        """
        if dst_repo_id is None:
            dst_repo_id = self.repo.id

        dirent_type = 'dir' if self.isdir else 'file'
        resp = self._copy_move_task('copy', dirent_type, dst_dir, dst_repo_id)
        return resp.status_code == 200

    def moveTo(self, dst_dir, dst_repo_id=None):
        """Move file/folder to other directory (also to a different repo)
        """
        if dst_repo_id is None:
            dst_repo_id = self.repo.id

        dirent_type = 'dir' if self.isdir else 'file'
        resp = self._copy_move_task('move', dirent_type, dst_dir, dst_repo_id)
        succeeded = resp.status_code == 200
        if succeeded:
            new_repo = self.client.repos.get_repo(dst_repo_id)
            dst_path = os.path.join(dst_dir, os.path.basename(self.path))
            if self.isdir:
                new_dirent = new_repo.get_dir(dst_path)
            else:
                new_dirent = new_repo.get_file(dst_path)
            for key in self.__dict__.keys():
                self.__dict__[key] = new_dirent.__dict__[key]
        return succeeded

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

    def share_to_user(self, email, permission):
        url = '/api2/repos/%s/dir/shared_items/' % self.repo.id + querystr(p=self.path)
        putdata = {
            'share_type': 'user',
            'username': email,
            'permission': permission
        }
        resp = self.client.put(url, data=putdata)
        return resp.status_code == 200

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
