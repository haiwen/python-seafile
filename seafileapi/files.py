import io
import os
import posixpath
import re
from .utils import querystr, utf8lize, urlencode, urljoin

ZERO_OBJ_ID = '0000000000000000000000000000000000000000'

class _SeafDirentBase(object):
    """Base class for :class:`SeafFile` and :class:`SeafDir`.

    It provides implementation of their common oqperations.
    """
    isdir = None

    def __init__(self, repo, name, type, id=None, parent_dir=None, size=None):
        """
        :param:`repo` repository object
        :param:'name' name of file or directory
        :param:'type' dir or file
        :param:'id' id of object
        :param:'parent_dir' path of upstream directory. If there is no upstream dir, parent_dir should be '/'
        :param:`size` The size of a file. It should be zero for a dir.
        """
        self.repo = repo
        self.path = '/'+ name
        self.id = id if id is not None else ZERO_OBJ_ID
        self.name=name
        self.parent_dir = parent_dir if parent_dir is not None else '/'
        self.type = type
        self.size = size
        self.full_path = urljoin(self.parent_dir, self.path)

    def __str__(self):
        return f"_SeafDirentBase[{self.type}: {self.name}, path: {self.full_path}]"
    __repr__ = __str__

    @classmethod
    def from_json(cls, repo, dir_json):
        dir_json = utf8lize(dir_json)

        repo=repo
        name = dir_json['name']
        id = dir_json['id']
        parent_dir = dir_json.get('parent_dir', '/')
        type = dir_json['type']
        size = dir_json.get('size', 0)

        return cls(repo, name, type, id, parent_dir, size)

    def list_revisions(self):
        pass

    def delete(self):
        suffix = 'dir' if self.isdir else 'file'
        url = '/api2/repos/%s/%s/' % (self.repo.id, suffix) + querystr(p=self.path)
        resp = self.repo.client.delete(url)
        return resp

    def rename(self, newname):
        """
        Change file/folder name to newname
        """
        suffix = 'dir' if self.isdir else 'file'
        url = '/api2/repos/%s/%s/' % (self.repo.id, suffix) + querystr(p=self.path, reloaddir='true')
        postdata = {'operation': 'rename', 'newname': newname}
        resp = self.repo.client.post(url, data=postdata)
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
        return self.repo.client.post(url, data=postdata)

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
            new_repo = self.repo.client.repos.get_repo(dst_repo_id)
            dst_path = os.path.join(dst_dir, os.path.basename(self.path))
            if self.isdir:
                new_dirent = new_repo.get_dir(dst_path)
            else:
                new_dirent = new_repo.get_file(dst_path)
            for key in self.__dict__.keys():
                self.__dict__[key] = new_dirent.__dict__[key]
        return succeeded

    def get_share_link(self, can_edit=False, can_download=True, password=None, expire_days=None, direct_link=True):
        url = '/api/v2.1/share-links/'
        post_data = {
            "repo_id": self.repo.id,
            "path": self.path,
            "permissions": {
                "can_edit": can_edit,
                "can_download": can_download
            }
        }
        if password:
            post_data['password'] = password
        if expire_days:
            post_data['expire_days'] = expire_days

        resp = self.repo.client.post(url, data=post_data)
        link = resp.json()['link']
        if direct_link:
            link = link + '?dl=1'

        return link

    def _get_upload_link(self):
        """
        get upload link of a file or directory. If object is a file, the file will be uploaded to parent dir. 
        If object is a directory, upload link will be created for itself
        """
        url = '/api2/repos/%s/upload-link/' % self.repo.id
        query = '?'+urlencode(dict(p=self.parent_dir if self.type=='file' else self.full_path))
        resp = self.repo.client.get(url+query)
        return re.match(r'"(.*)"', resp.text).group(1)


class SeafDir(_SeafDirentBase):
    isdir = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entries = None
        self.entries = kwargs.pop('entries', None)

    def ls(self, force_refresh=False):
        """List the entries in this dir.

        Return a list of objects of class :class:`SeafFile` or :class:`SeafDir`.
        """
        if self.entries is None or force_refresh:
            self.load_entries(type="d")

        return self.entries

    def share_to_user(self, email, permission):
        """
            share dir to other user.
            :param: email of other user
            :param: permission should be 'r' for read and 'rw' for read and write
        """
        url = '/api2/repos/%s/dir/shared_items/' % self.repo.id + querystr(p=self.path)
        putdata = {
            'share_type': 'user',
            'username': email,
            'permission': permission
        }
        resp = self.repo.client.put(url, data=putdata)
        return resp.status_code == 200

    def create_empty_file(self, name):
        """Create a new empty file in this dir.
        Return a :class:`SeafFile` object of the newly created file.
        """
        # TODO: file name validation
        path = posixpath.join(self.path, name)
        url = '/api2/repos/%s/file/' % self.repo.id + querystr(p=path, reloaddir='true')
        postdata = {'operation': 'create'}
        resp = self.repo.client.post(url, data=postdata)
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
        resp = self.repo.client.post(url, data=postdata)
        self.id = resp.headers['oid']
        self.load_entries(resp.json())
        return SeafDir(self.repo, path, ZERO_OBJ_ID)

    def upload(self, fileobj, filename, replace=False):
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
            'replace': 1 if replace else 0,
        }
        self.repo.client.post(upload_url, files=files)
        return self.repo.get_file(posixpath.join(self.path, filename))

    def upload_local_file(self, filepath, name=None, replace=False):
        """Upload a file to this folder.

        :param:filepath The path to the local file
        :param:name The name of this new file. If None, the name of the local file would be used.

        Return a :class:`SeafFile` object of the newly uploaded file.
        """
        name = name or os.path.basename(filepath)
        with open(filepath, 'r') as fp:
            return self.upload(fp, name, replace)

    def get_uploadable_sharelink(self):
        """Generate a uploadable shared link to this dir.

        Return the url of this link.
        """
        pass

    def load_entries(self, dirents_json=None, type=None):
        if dirents_json is None:
            url = '/api2/repos/%s/dir/' % self.repo.id
            # oid: object id-id of upstream dir
            # t: type - must be f for file or d for dir
            if type is None:
                query = '?' + urlencode(dict(oid=self.id, recursive=1))
            else:
                query = '?' + urlencode(dict(oid=self.id, recursive=1, t=type))
            dirents_json = self.repo.client.get(url+query).json()

        self.entries = [self._load_dirent(entry_json) for entry_json in dirents_json]

    def _load_dirent(self, dirent_json):
        dirent_json = utf8lize(dirent_json)
        path = posixpath.join(self.path, dirent_json['name'])
        if dirent_json['type'] == 'file':
            return SeafFile(self.repo, dirent_json['name'],dirent_json['type'], dirent_json['id'], dirent_json['parent_dir'], dirent_json.get('size', 0))
        else:
            return SeafDir(self.repo, dirent_json['name'],dirent_json['type'], dirent_json['id'], dirent_json['parent_dir'], dirent_json.get('size', 0))

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
        url = '/api2/repos/%s/file/' % self.repo.id + querystr(p=self.full_path,reuse=1)
        resp = self.repo.client.get(url)
        return re.match(r'"(.*)"', resp.text).group(1)

    def get_content(self):
        """Get the content of the file"""
        url = self._get_download_link()
        return self.repo.client.get(url).content

    __repr__ = __str__
