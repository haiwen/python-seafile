#coding: UTF-8

import unittest
import seafileapi

class PySeafileTestCase(unittest.TestCase):
    user = 'test@seafiletest.com'
    password = 'testtest'

    def test_connect(self):
        client = seafileapi.SeafileApiClient('http://127.0.0.1:8000', self.user, self.password)
