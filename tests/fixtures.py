#coding: utf-8

import os
import pytest

import seafileapi
from tests.utils import randstring

SERVER = os.environ.get('SEAFILE_TEST_SERVER_ADDRESS', 'http://192.168.1.202:8000')
USER = os.environ.get('SEAFILE_TEST_USERNAME', 'commissarster@qq.com')
PASSWORD = os.environ.get('SEAFILE_TEST_PASSWORD', 'commissar')
ADMIN_USER = os.environ.get('SEAFILE_TEST_ADMIN_USERNAME', 'commissarster@qq.com')
ADMIN_PASSWORD = os.environ.get('SEAFILE_TEST_ADMIN_PASSWORD', 'commissar')

@pytest.fixture(scope='session')
def client():
    return seafileapi.connect(SERVER, USER, PASSWORD)

@pytest.yield_fixture(scope='function')
def repo(client):
    repo_name = 'tmp-测试资料库-%s' % randstring()
    repo_desc = 'tmp, 一个测试资料库-%s' % randstring()
    repo = client.repos.create_repo(repo_name, repo_desc)
    try:
        yield repo
    finally:
        repo.delete()
