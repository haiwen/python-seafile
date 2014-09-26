import os
import seafileapi
import unittest

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
