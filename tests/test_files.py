#coding: UTF-8

import os
import pytest

from tests.utils import randstring, datafile, filesize

@pytest.mark.parametrize('parentpath', [
    '/',
    '/测试目录一-%s' % randstring()
])
def test_create_delete_file_dir(repo, parentpath):
    rootdir = repo.get_dir('/')
    assert len(rootdir.ls(force_refresh=True)) == 0

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
    assert len(parentdir.ls(force_refresh=True)) == 2
    assert len(testdir.ls(force_refresh=True)) == 0

    direntry = [e for e in parentdir.ls(force_refresh=True) if e.isdir][0]
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
    assert len(rootdir.ls(force_refresh=True)) == 0

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

@pytest.mark.parametrize('parentpath', [
    '/',
    #'/测试目录一-%s' % randstring()
    '/qweqwe%s' % randstring()
])
def test_rename_file(repo, parentpath):
    rootdir = repo.get_dir('/')
    assert len(rootdir.ls(force_refresh=True)) == 0

    if parentpath == '/':
        parentdir = rootdir
    else:
        parentdir = rootdir.mkdir(parentpath[1:])

    # create a file
    testfile = parentdir.create_empty_file('测试文件-%s.txt' % randstring())
    assert testfile.size == 0

    assert len(parentdir.ls(force_refresh=True)) == 1

    # rename a file
    newfname = 'newfile.txt'
    testfile.rename(newfname)
    assert newfname == testfile.name

@pytest.mark.parametrize('parentpath', [
    '/',
    '/测试目录一-%s' % randstring()
])
def test_rename_folder(repo, parentpath):
    rootdir = repo.get_dir('/')
    assert len(rootdir.ls(force_refresh=True)) == 0

    if parentpath == '/':
        parentdir = rootdir
    else:
        parentdir = rootdir.mkdir(parentpath[1:])

    # create a folder
    testfolder = parentdir.mkdir('测试文件夹-%s' % randstring())
    assert testfolder.size == 0

    assert len(parentdir.ls(force_refresh=True)) == 1

    # rename a file
    newfname = 'newfolder'
    testfolder.rename(newfname)
    assert newfname == testfolder.name

@pytest.mark.parametrize('parentpath', [
    '/',
    '/测试目录一-%s' % randstring()
])
def test_copy_file(repo, parentpath):
    rootdir = repo.get_dir('/')
    assert len(rootdir.ls(force_refresh=True)) == 0

    if parentpath == '/':
        parentdir = rootdir
    else:
        parentdir = rootdir.mkdir(parentpath[1:])

    # create a file
    testfile = parentdir.create_empty_file('测试文件-%s.txt' % randstring())
    assert testfile.size == 0

    assert len(parentdir.ls(force_refresh=True)) == 1

    tempfolder = parentdir.mkdir('tempfolder_%s' % randstring())
    assert len(tempfolder.ls(force_refresh=True)) == 0
    testfile.copyTo(tempfolder.path)
    assert len(tempfolder.ls(force_refresh=True)) == 1
    assert os.path.basename(tempfolder.ls(force_refresh=True)[-1].path) == os.path.basename(testfile.path)

@pytest.mark.parametrize('parentpath', [
    '/',
    '/测试目录一-%s' % randstring()
])
def test_copy_file_to_other_repo(client, repo, parentpath):
    rootdir = repo.get_dir('/')
    assert len(rootdir.ls(force_refresh=True)) == 0

    if parentpath == '/':
        parentdir = rootdir
    else:
        parentdir = rootdir.mkdir(parentpath[1:])

    # create a file
    testfile = parentdir.create_empty_file('测试文件-%s.txt' % randstring())
    assert testfile.size == 0

    assert len(parentdir.ls(force_refresh=True)) == 1

    temp_repo = client.repos.create_repo('temp_repo')
    try:
        root_dir = temp_repo.get_dir('/')
        temp_dir = root_dir.mkdir('temp_dir')
        assert len(temp_dir.ls(force_refresh=True)) == 0
        testfile.copyTo(temp_dir.path, temp_repo.id)
        assert len(temp_dir.ls(force_refresh=True)) == 1
        assert os.path.basename(temp_dir.ls(force_refresh=True)[0].path) == os.path.basename(testfile.path)
    finally:
        temp_repo.delete()

@pytest.mark.parametrize('parentpath', [
    '/',
    '/测试目录一-%s' % randstring()
])
def test_copy_folder(repo, parentpath):
    rootdir = repo.get_dir('/')
    assert len(rootdir.ls(force_refresh=True)) == 0

    if parentpath == '/':
        parentdir = rootdir
    else:
        parentdir = rootdir.mkdir(parentpath[1:])

    # create a folder
    testfolder = parentdir.mkdir('测试文件夹-%s' % randstring())
    assert testfolder.size == 0
    tempfolder = parentdir.mkdir('temp-folder-%s' % randstring())
    assert tempfolder.size == 0

    assert len(tempfolder.ls(force_refresh=True)) == 0
    assert len(parentdir.ls(force_refresh=True)) == 2

    # copy a file
    testfolder.copyTo(tempfolder.path)
    assert len(tempfolder.ls(force_refresh=True)) == 1
    assert os.path.basename(tempfolder.ls(force_refresh=True)[0].path) == os.path.basename(testfolder.path)

@pytest.mark.parametrize('parentpath', [
    '/',
    '/测试目录一-%s' % randstring()
])
def test_copy_folder_to_other_repo(client, repo, parentpath):
    rootdir = repo.get_dir('/')
    assert len(rootdir.ls(force_refresh=True)) == 0

    if parentpath == '/':
        parentdir = rootdir
    else:
        parentdir = rootdir.mkdir(parentpath[1:])

    # create a folder
    testfolder = parentdir.mkdir('测试文件夹-%s' % randstring())
    assert testfolder.size == 0

    assert len(parentdir.ls(force_refresh=True)) == 1

    temp_repo = client.repos.create_repo('temp_repo')
    try:
        root_folder = temp_repo.get_dir('/')
        tempfolder = root_folder.mkdir('tempfolder')

        assert len(tempfolder.ls(force_refresh=True)) == 0
        # copy a folder
        testfolder.copyTo(tempfolder.path, temp_repo.id)
        assert len(tempfolder.ls(force_refresh=True)) == 1
        assert os.path.basename(tempfolder.ls(force_refresh=True)[0].path) == os.path.basename(testfolder.path)
    finally:
        temp_repo.delete()

@pytest.mark.parametrize('parentpath', [
    '/',
    '/测试目录一-%s' % randstring()
])
def test_move_file(repo, parentpath):
    rootdir = repo.get_dir('/')
    assert len(rootdir.ls(force_refresh=True)) == 0

    if parentpath == '/':
        parentdir = rootdir
    else:
        parentdir = rootdir.mkdir(parentpath[1:])

    # create a file
    testfile = parentdir.create_empty_file('测试文件-%s.txt' % randstring())
    assert testfile.size == 0

    assert len(parentdir.ls(force_refresh=True)) == 1

    tempfolder = parentdir.mkdir('tempfolder_%s' % randstring())
    assert len(tempfolder.ls(force_refresh=True)) == 0

    testfile.moveTo(tempfolder.path)
    assert testfile.path == os.path.join(tempfolder.path, os.path.basename(testfile.path))
    assert len(tempfolder.ls(force_refresh=True)) == 1

@pytest.mark.parametrize('parentpath', [
    '/',
    '/测试目录一-%s' % randstring()
])
def test_move_file_to_other_repo(client, repo, parentpath):
    rootdir = repo.get_dir('/')
    assert len(rootdir.ls(force_refresh=True)) == 0

    if parentpath == '/':
        parentdir = rootdir
    else:
        parentdir = rootdir.mkdir(parentpath[1:])

    # create a file
    testfile = parentdir.create_empty_file('测试文件-%s.txt' % randstring())
    assert testfile.size == 0

    assert len(parentdir.ls(force_refresh=True)) == 1

    temp_repo = client.repos.create_repo('temp_repo')
    try:
        root_dir = temp_repo.get_dir('/')
        temp_dir = root_dir.mkdir('temp_dir')
        assert len(temp_dir.ls(force_refresh=True)) == 0
        testfile.moveTo(temp_dir.path, temp_repo.id)
        assert testfile.path == os.path.join(temp_dir.path, os.path.basename(testfile.path))
        assert len(temp_dir.ls(force_refresh=True)) == 1
        assert testfile.repo.id == temp_repo.id
    finally:
        temp_repo.delete()

@pytest.mark.parametrize('parentpath', [
    '/',
    '/测试目录一-%s' % randstring()
])
def test_move_folder(repo, parentpath):
    rootdir = repo.get_dir('/')
    assert len(rootdir.ls(force_refresh=True)) == 0

    if parentpath == '/':
        parentdir = rootdir
    else:
        parentdir = rootdir.mkdir(parentpath[1:])

    # create a folder
    testfolder = parentdir.mkdir('测试文件夹-%s' % randstring())
    assert testfolder.size == 0
    tempfolder = parentdir.mkdir('temp-folder-%s' % randstring())
    assert tempfolder.size == 0

    assert len(parentdir.ls(force_refresh=True)) == 2

    # move a folder
    testfolder.moveTo(tempfolder.path)
    assert testfolder.path == os.path.join(tempfolder.path, os.path.basename(testfolder.path))

@pytest.mark.parametrize('parentpath', [
    '/',
    '/测试目录一-%s' % randstring()
])
def test_move_folder_to_other_repo(client, repo, parentpath):
    rootdir = repo.get_dir('/')
    assert len(rootdir.ls(force_refresh=True)) == 0

    if parentpath == '/':
        parentdir = rootdir
    else:
        parentdir = rootdir.mkdir(parentpath[1:])

    # create a folder
    testfolder = parentdir.mkdir('测试文件夹-%s' % randstring())
    assert testfolder.size == 0

    assert len(parentdir.ls(force_refresh=True)) == 1

    temp_repo = client.repos.create_repo('temp_repo')
    try:
        root_folder = temp_repo.get_dir('/')
        tempfolder = root_folder.mkdir('tempfolder')

        assert len(tempfolder.ls(force_refresh=True)) == 0
        # move a folder
        testfolder.moveTo(tempfolder.path, temp_repo.id)
        assert testfolder.path == os.path.join(tempfolder.path, os.path.basename(testfolder.path))
        assert testfolder.repo.id == temp_repo.id
        assert len(tempfolder.ls(force_refresh=True)) == 1
    finally:
        temp_repo.delete()
