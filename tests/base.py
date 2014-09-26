#coding: UTF-8

import os
import seafileapi
import unittest
from contextlib import contextmanager
from tests.utils import randstring

SERVER = os.environ.get('SEAFILE_TEST_SERVER_ADDRESS', 'http://127.0.0.1:8000')
USER = os.environ.get('SEAFILE_TEST_USERNAME', 'test@seafiletest.com')
PASSWORD = os.environ.get('SEAFILE_TEST_PASSWORD', 'testtest')
ADMIN_USER = os.environ.get('SEAFILE_TEST_ADMIN_USERNAME', 'admin@seafiletest.com')
ADMIN_PASSWORD = os.environ.get('SEAFILE_TEST_ADMIN_PASSWORD', 'adminadmin')

def _create_client():
    return seafileapi.connect(SERVER, USER, PASSWORD)

class SeafileApiTestCase(unittest.TestCase):
    """Base class for all python-seafile test cases"""
    @classmethod
    def setupClass(cls):
        cls.client = _create_client()

    def assertHasLen(self, obj, expected_length):
        actuallen = len(obj)
        msg = 'Expected length is %s, but actual lenght is %s' % (expected_length, actuallen)
        self.assertEqual(actuallen, expected_length, msg)

    @contextmanager
    def create_tmp_repo(self):
        repos = self.client.repos
        repo_name = 'tmp-测试资料库-%s' % randstring()
        repo_desc = 'tmp, 一个测试资料库-%s' % randstring()
        repo = repos.create_repo(repo_name, repo_desc)

        try:
            yield repo
        finally:
            repo.delete()

