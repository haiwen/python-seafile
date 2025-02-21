import os
import json
import requests

from seafileapi.exceptions import ClientHttpError
from seafileapi.utils import urljoin


def parse_headers(token):
    return {
        'Authorization': 'Token ' + token,
        'Content-Type': 'application/json',
    }


def parse_response(response):
    if response.status_code >= 400:
        raise ConnectionError(response.status_code, response.text)
    else:
        try:
            data = json.loads(response.text)
            return data
        except Exception:
            pass


class Repo(object):

    def __init__(self, token, server_url):

        self.server_url = server_url
        self.token = token
        self.repo_id = None
        self.timeout = 30
        self.headers = None

        self._by_api_token = True

    def auth(self, by_api_token=True):
        if not by_api_token:
            self._by_api_token = False
        self.headers = parse_headers(self.token)

    def _repo_info_url(self):
        if self._by_api_token:
            return "%s/%s" % (self.server_url.rstrip('/'), 'api/v2.1/via-repo-token/repo-info/')

        return "%s/%s" % (self.server_url.rstrip('/'), 'api/v2.1/repos/%s/' % self.repo_id)

    def _repo_dir_url(self):
        if self._by_api_token:
            return "%s/%s" % (self.server_url.rstrip('/'), 'api/v2.1/via-repo-token/dir/')

        return "%s/%s" % (self.server_url.rstrip('/'), 'api/v2.1/repos/%s/dir/' % self.repo_id)

    def _repo_file_url(self):
        if self._by_api_token:
            return "%s/%s" % (self.server_url.rstrip('/'), 'api/v2.1/via-repo-token/file/')

        return "%s/%s" % (self.server_url.rstrip('/'), 'api/v2.1/repos/%s/file/' % self.repo_id)

    def _repo_upload_link_url(self):
        if self._by_api_token:
            return "%s/%s" % (self.server_url.rstrip('/'), 'api/v2.1/via-repo-token/upload-link/')

        return "%s/%s" % (self.server_url.rstrip('/'), 'api2/repos/%s/upload-link/' % self.repo_id)

    def _repo_download_link_url(self):
        if self._by_api_token:
            return "%s/%s" % (self.server_url.rstrip('/'), 'api/v2.1/via-repo-token/download-link/')

        return "%s/%s" % (self.server_url.rstrip('/'), 'api2/repos/%s/file/' % self.repo_id)

    def get_repo_details(self):
        url = self._repo_info_url()
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        repo = parse_response(response)
        return {
            'repo_id': repo.get('repo_id'),
            'repo_name': repo.get('repo_name'),
            'size': repo.get('size'),
            'file_count': repo.get('file_count'),
            'last_modified': repo.get('last_modified'),
        }

    def list_dir(self, dir_path='/'):
        url = self._repo_dir_url()
        params = {
            'p': dir_path,
            'path': dir_path
        }
        response = requests.get(url, params=params, headers=self.headers, timeout=self.timeout)
        resp = parse_response(response)
        return resp['dirent_list']

    def create_dir(self, path):
        # / api2 / repos / {repo_id} / dir /
        url = self._repo_dir_url()
        params = {'path': path} if '/via-repo-token' in url else {'p': path}
        data = {
            'operation': 'mkdir',
        }
        response = requests.post(url, params=params, json=data, headers=self.headers, timeout=self.timeout)
        return parse_response(response)

    def rename_dir(self, path, newname):
        url = self._repo_dir_url()
        params = {'path': path} if '/api/v2.1/via-repo-token' in url else {'p': path}
        data = {
            'operation': 'rename',
            'newname': newname
        }
        response = requests.post(url, params=params, json=data, headers=self.headers, timeout=self.timeout)
        return parse_response(response)

    def delete_dir(self, path):
        url = self._repo_dir_url()
        params = {'path': path} if '/via-repo-token' in url else {'p': path}
        response = requests.delete(url, params=params, headers=self.headers, timeout=self.timeout)
        return parse_response(response)

    def get_file(self, path):
        # /api2/repos/{repo_id}/file/detail/
        url = self._repo_file_url() \
            if '/via-repo-token' in self._repo_file_url() \
            else urljoin(self.server_url, 'api2/repos/%s/file/detail/' % self.repo_id)
        params = {'path': path} if '/via-repo-token' in url else {"p": path}
        response = requests.get(url, params=params, headers=self.headers, timeout=self.timeout)
        return parse_response(response)

    def create_file(self, path):
        url = self._repo_file_url()
        params = {'path': path} if '/via-repo-token' in url else {'p': path}
        data = {
            "operation": "create"
        }
        response = requests.post(url, params=params, json=data, headers=self.headers, timeout=self.timeout)
        return parse_response(response)

    def rename_file(self, path, newname):
        """
        Rename a file
        :param path: file path
        :param newname:file newname
        :return:
        """
        url = self._repo_file_url()
        params = {'path': path} if '/via-repo-token' in url else {'p': path}
        data = {
            "operation": "rename",
            "newname": newname
        }
        response = requests.post(url, params=params, json=data, headers=self.headers, timeout=self.timeout)
        return parse_response(response)

    def delete_file(self, path):
        """
        Delete a file/folder
        :param p: file/folder path
        :return:{'success': True, 'commit_id': '2147035976f20495fdc0a85f1a8a9c109b22c97d'}
        """
        url = self._repo_file_url()
        params = {'path': path} if '/via-repo-token' in url else {'p': path}
        response = requests.delete(url, params=params, headers=self.headers, timeout=self.timeout)
        return parse_response(response)

    def upload_file(self, parent_dir, file_path):
        upload_link_url = self._repo_upload_link_url()
        params = {'path': parent_dir} if '/via-repo-token' in upload_link_url else {'p': parent_dir}
        response = requests.get(upload_link_url, params=params, headers=self.headers, timeout=self.timeout)
        upload_link = response.text.strip('"')
        upload_link = "%s?ret-json=1" % upload_link
        files = {'file': open(file_path, 'rb')}
        data = {'parent_dir': parent_dir}
        response = requests.post(upload_link, files=files, data=data)
        if response.status_code == 200:
            return response.json()[0]
        else:
            raise Exception('upload file error')

    def download_file(self, file_path, save_path):
        url = self._repo_download_link_url()
        params = {'path': file_path} if '/via-repo-token' in url else {'p': file_path}
        response = requests.get(url, params=params, headers=self.headers)

        file_download_url = response.json()
        response = requests.get(file_download_url, headers=self.headers)

        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
        else:
            raise Exception('download file error')


class SeafileAPI(object):

    def __init__(self, login_name, password, server_url):
        self.login_name = login_name
        self.username = None
        self.password = password
        self.server_url = server_url.strip().strip('/')
        self.token = None
        self.timeout = 30

        self.headers = None

    def auth(self):
        data = {
            'username': self.login_name,
            'password': self.password,
        }
        url = "%s/%s" % (self.server_url.rstrip('/'), 'api2/auth-token/')
        res = requests.post(url, data=data, timeout=self.timeout)
        if res.status_code != 200:
            raise ClientHttpError(res.status_code, res.content)
        token = res.json()['token']
        assert len(token) == 40, 'The length of seahub api auth token should be 40'
        self.token = token
        self.headers = parse_headers(token)

    def _repo_obj(self, repo_id):
        repo = Repo(self.token, self.server_url)
        repo.repo_id = repo_id
        repo.auth(by_api_token=False)

        return repo

    def list_repos(self):
        url = urljoin(self.server_url, 'api2/repos')
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        return parse_response(response)

    def get_repo(self, repo_id):
        url = urljoin(self.server_url, 'api2/repos/%s' % repo_id)
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        data = parse_response(response)
        repo_id = data.get('id')
        return self._repo_obj(repo_id)

    def create_repo(self, repo_name, passwd=None, story_id=None):
        url = urljoin(self.server_url, 'api2/repos/')
        data = {
            "name": repo_name,
        }
        if passwd:
            data['passwd'] = passwd
        if story_id:
            data['story_id'] = story_id
        response = requests.post(url, json=data, headers=self.headers, timeout=self.timeout)
        if response.status_code == 200:
            data = parse_response(response)
            repo_id = data.get('repo_id')
            return self._repo_obj(repo_id)

    def delete_repo(self, repo_id):
        """Remove this repo. Only the repo owner can do this"""
        url = urljoin(self.server_url, '/api2/repos/%s/' % repo_id)
        requests.delete(url, headers=self.headers, timeout=self.timeout)
        return True
