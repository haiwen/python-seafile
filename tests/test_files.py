#coding: UTF-8

import unittest
from seafileapi import client
from seafileapi.exceptions import DoesNotExist
from seafileapi.files import SeafFile, SeafDir
from tests.base import SeafileApiTestCase
from tests.utils import randstring, datafile, filesize

class FilesTest(SeafileApiTestCase):
    def test_create_delete_file_dir(self):
        with self.create_tmp_repo() as repo:
            def test_under_parentpath(parentpath='/'):
                rootdir = repo.get_dir('/')
                self.assertHasLen(rootdir.ls(), 0)

                if parentpath == '/':
                    parentdir = rootdir
                else:
                    parentdir = rootdir.mkdir(parentpath[1:])

                # create a file
                testfile = parentdir.create_empty_file('测试文件-%s.txt' % randstring())
                self.assertEqual(testfile.size, 0)

                entries = parentdir.ls(force_refresh=True)
                self.assertEqual(len(entries), 1)

                entry = entries[0]
                self.assertEqual(entry.path, testfile.path)
                self.assertEqual(entry.id, testfile.id)
                self.assertEqual(entry.size, testfile.size)

                # create a folder
                testdir = parentdir.mkdir('测试目录-%s' % randstring())
                self.assertHasLen(parentdir.ls(), 2)
                self.assertHasLen(testdir.ls(), 0)

                direntry = [entry for entry in parentdir.ls() if entry.isdir][0]
                self.assertEqual(direntry.path, testdir.path)

                testfile.delete()
                self.assertHasLen(parentdir.ls(force_refresh=True), 1)
                testdir.delete()
                self.assertHasLen(parentdir.ls(force_refresh=True), 0)

            test_under_parentpath()
            test_under_parentpath(parentpath='/测试目录一-%s' % randstring())

    def test_upload_file(self):
        with self.create_tmp_repo() as repo:
            def test_under_parentpath(parentpath='/'):
                rootdir = repo.get_dir('/')
                self.assertHasLen(rootdir.ls(), 0)

                if parentpath == '/':
                    parentdir = rootdir
                else:
                    parentdir = rootdir.mkdir(parentpath[1:])

                fname = 'aliedit.tar.gz'
                fpath = datafile(fname)
                with open(fpath, 'r') as fp:
                    testfile = parentdir.upload(fp, fname)

                with open(fpath, 'r') as fp:
                    fcontent = fp.read()

                self.assertEqual(testfile.size, filesize(fpath))
                self.assertEqual(testfile.name, fname)
                self.assertEqual(testfile.repo.id, repo.id)
                assert testfile.get_content() == fcontent, \
                    'uploaded file content should be the same with the original file'
                entries = parentdir.ls(force_refresh=True)
                self.assertEqual(len(entries), 1)

                entry = entries[0]
                self.assertEqual(entry.path, testfile.path)
                self.assertEqual(entry.id, testfile.id)
                self.assertEqual(entry.size, testfile.size)

                testfile.delete()
                self.assertEmpty(parentdir.ls(force_refresh=True))

            test_under_parentpath()
            test_under_parentpath(parentpath='/测试目录一-%s' % randstring())

            # test pass as string as file content when upload file
            rootdir = repo.get_dir('/')
            fname = u'testfile-%s' % randstring()
            fcontent = 'line 1\nline 2\n\r'
            f = rootdir.upload(fcontent, fname)
            assert f.name == fname
            assert f.get_content() == fcontent
