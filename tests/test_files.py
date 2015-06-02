#coding: UTF-8

import pytest

from tests.utils import randstring, datafile, filesize

@pytest.mark.parametrize('parentpath', [
    '/',
    '/测试目录一-%s' % randstring()
])
def test_create_delete_file_dir(repo, parentpath):
    rootdir = repo.get_dir('/')
    assert len(rootdir.ls()) == 0

    if parentpath == '/':
        parentdir = rootdir
    else:
        parentdir = rootdir.mkdir(parentpath[1:])

    # create a file
    testfile = parentdir.create_empty_file('测试文件-%s.txt' % randstring())
    assert testfile.size == 0

    entries = parentdir.ls(force_refresh=True)
    assert len(entries) == 1

    entry = entries[0]
    assert entry.path == testfile.path
    assert entry.id == testfile.id
    assert entry.size == testfile.size

    # create a folder
    testdir = parentdir.mkdir('测试目录-%s' % randstring())
    assert len(parentdir.ls()) == 2
    assert len(testdir.ls()) == 0

    direntry = [entry for entry in parentdir.ls() if entry.isdir][0]
    assert direntry.path == testdir.path

    testfile.delete()
    assert len(parentdir.ls(force_refresh=True)) == 1
    testdir.delete()
    assert len(parentdir.ls(force_refresh=True)) == 0


@pytest.mark.parametrize('parentpath', [
    '/',
    '/测试目录一-%s' % randstring()
])
def test_upload_file(repo, parentpath):
    rootdir = repo.get_dir('/')
    assert len(rootdir.ls()) == 0

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

    assert testfile.size == filesize(fpath)
    assert testfile.name == fname
    assert testfile.repo.id == repo.id
    assert testfile.get_content() == fcontent, \
        'uploaded file content should be the same with the original file'
    entries = parentdir.ls(force_refresh=True)
    assert len(entries) == 1

    entry = entries[0]
    assert entry.path == testfile.path
    assert entry.id == testfile.id
    assert entry.size == testfile.size

    testfile.delete()
    assert len(parentdir.ls(force_refresh=True)) == 0

def test_upload_string_as_file_content(repo):
    # test pass as string as file content when upload file
    rootdir = repo.get_dir('/')
    fname = u'testfile-%s' % randstring()
    fcontent = 'line 1\nline 2\n\r'
    f = rootdir.upload(fcontent, fname)
    assert f.name == fname
    assert f.get_content() == fcontent

'/测试目录一-%s' % randstring()
@pytest.mark.parametrize('parentpath', [
    '/',
    '/seafdir-%s' % randstring()
])
def test_rename_move_copy(repo, parentpath):
    rootdir = repo.get_dir('/')
    assert len(rootdir.ls()) == 0

    if parentpath == '/':
        parentdir = rootdir
    else:
        parentdir = rootdir.mkdir(parentpath[1:])

    # create a file
    testfile = parentdir.create_empty_file('测试文件-%s.txt' % randstring())
    assert testfile.size == 0

    entries = parentdir.ls(force_refresh=True)
    assert len(entries) == 1

    entry = entries[0]
    assert entry.path == testfile.path
    assert entry.id == testfile.id
    assert entry.size == testfile.size

    # rename a file
    newfname = 'newfile.txt'
    testfile.rename(newfname)
    assert testfile.name == newfname

    # create a folder
    testdir = parentdir.mkdir('测试目录-%s' % randstring())
    assert len(parentdir.ls()) == 2
    assert len(testdir.ls()) == 0

    direntry = [entry for entry in parentdir.ls() if entry.isdir][0]
    assert direntry.path == testdir.path

    # move a file to the new folder
    testfile.moveTo(testdir.name, dst_repo=None)

    assert testfile.name == newfname
    fileentry = [entry for entry in testdir.ls() if not entry.isdir][0]
    assert fileentry.path == testfile.path

    # copy a file to the parent folder
    filenames.append(testfile)
    testfile.copyTo(filenames, parentdir.name, dst_repo=None)

    assert testfile.name == newfname
    fileentry = [entry for entry in parentdir.ls() if not entry.isdir][0]
    assert fileentry.path == testfile.path

    # clean up test directories / files
    testfile.delete()
    assert len(parentdir.ls(force_refresh=True)) == 1
    testdir.delete()
    assert len(parentdir.ls(force_refresh=True)) == 0
