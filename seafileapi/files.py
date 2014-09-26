

class _SeafDirentBase(object):
    def __init__(self, client, repo, path):
        self.client = client
        self.repo = repo
        self.path = path

    def list_revisions(self):
        pass

    def delete(self):
        pass

    def rename(self):
        pass

    def copyTo(self, dst_dir, dst_repo=None):
        pass

    def moveTo(self, dst_dir, dst_repo=None):
        pass

    def get_share_link(self):
        pass

class SeafDir(_SeafDirentBase):
    def upload(self, fileobj, filename):
        """Upload a file to this folder"""
        pass

    def get_upload_link(self):
        pass

class SeafFile(object):
    def update(self, fileobj):
        """Update the content of this file"""
        pass
