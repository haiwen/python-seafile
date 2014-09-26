#coding: UTF-8

import unittest
from seafileapi import client
from seafileapi.exceptions import DoesNotExist
from tests.base import SeafileApiTestCase
from tests.utils import randstring

class ReposTest(SeafileApiTestCase):
    def test_create_delete_repo(self):
        repo = self._create_repo()
        repo.delete()

        with self.assertRaises(DoesNotExist):
            self.client.repos.get_repo(repo.id)

    def test_create_encrypted_repo(self):
        repo = self._create_repo(password=randstring())
        repo.delete()
        with self.assertRaises(DoesNotExist):
            self.client.repos.get_repo(repo.id)

    def _create_repo(self, password=None):
        repos = self.client.repos
        repo_name = '测试资料库-%s' % randstring()
        repo_desc = '一个测试资料库-%s' % randstring()
        repo = repos.create_repo(repo_name, repo_desc, password=password)

        self.assertEqual(repo.name, repo_name)
        self.assertEqual(repo.desc, repo_desc)
        self.assertHasLen(repo.id, 36)
        self.assertEqual(repo.encrypted, password != None)
        self.assertEqual(repo.owner, 'self')

        return repo

    def test_list_repos(self):
        repos = self.client.repos.list_repos()
        for repo in repos:
            self.assertHasLen(repo.id, 36)
