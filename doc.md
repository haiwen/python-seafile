# Python Seafile
<p><div class="doc">
<ul>
<li><a href="#get_client">Get Client</a></li>
<li>
	<a href="#seaffile">SeafFile</a>
	<ul>
		<li><a href="#seaffile_get_content">Get Content</a></li>
		<li><a href="#seaffile_delete">Delete file</a></li>
	</ul>
</li>
<li>
	<a href="#seafdir">SeafDir</a>
	<ul>
		<li><a href="#seafdir_ls">List</a></li>
		<li><a href="#seafdir_create_empty_file">Create Empty File</a></li>
		<li><a href="#seafdir_mkdir">Create New Folder</a></li>
		<li><a href="#seafdir_upload">Upload File</a></li>
		<li><a href="#seafdir_upload_local_file">Upload Local File</a></li>
		<li><a href="#seafdir_delete">Delete folder</a></li>
	</ul>
</li>
<li>
	<a href="#repo"> Repo </a>
	<ul>
		<li><a href="#repo_from_json">From Json</a></li>
		<li><a href="#repo_is_readonly">Is ReadOnly </a></li>
		<li><a href="#repo_get_file">Get File </a></li>
		<li><a href="#repo_get_dir">Get Dir</a></li>
		<li><a href="#repo_delete">Delete Repo</a></li>
	</ul>
</li>
<li>
	<a href="#repos"> Repos </a>
	<ul>
		<li><a href="#repos_get_repo">Get Repo</a></li>
		<li><a href="#repos_list_repo">List Repo</a></li>
		<li><a href="#repos_create_repo">Create Repo</a></li>
	</ul>
</li>
</ul>
</div>
</p>

# Python Seafile
## <a id="get_client"></a> Get Client ##
**Request Parameters**

* server
* username
* password

**Sample Case**

```python

	import seafileapi
	
	client = seafileapi.connect('http://127.0.0.1:8000', 'test@admin.com', 'password')
```

**Return Type**

A Client Object

## <a id="seaffile"></a> SeafFile ##
### <a id="seaffile_get_content"></a> Get Content ###

**Request Parameters**

None

**Sample Case**



```python

    import seafileapi
	
    client = seafileapi.connect('http://127.0.0.1:8000', 'test@admin.com', 'password')
    repo = client.repos.get_repo('09c16e2a-ff1a-4207-99f3-1351c3f1e507')
    seaffile = repo.get_file('/root/test.md')
	
    content = seaffile.get_content()
```

**Return Type**

File Content

### <a id="seaffile_delete"></a> Delete a file ###
**Request Parameters**

None

**Sample Case**

```python

    import seafileapi
	
    client = seafileapi.connect('http://127.0.0.1:8000', 'test@admin.com', 'password')
    repo = client.repos.get_repo('09c16e2a-ff1a-4207-99f3-1351c3f1e507')
    seaffile = repo.get_file('/root/test.md')
	
    seaffile.delete()
```

**Return Type**

A Response Instance

## <a id="seafdir"></a> SeafDir ##
### <a id="seafdir_ls"></a> List ###
**Request Parameters**

* force_refresh (default False)

**Sample Case**

```python

    import seafileapi
	
    client = seafileapi.connect('http://127.0.0.1:8000', 'test@admin.com', 'password')
    repo = client.repos.get_repo('09c16e2a-ff1a-4207-99f3-1351c3f1e507')
    seafdir = repo.get_dir('/root')
	
    lst = seafdir.ls(force_refresh=True)
    print lst
    Out >>> [SeafDir[repo=01ccc4,path=/Seahub/6.1.x,entries=14],
             SeafDir[repo=01ccc4,path=/Seahub/6.2.2-pro,entries=1],
             SeafDir[repo=01ccc4,path=/Seahub/6.2.3,entries=15],
             SeafDir[repo=01ccc4,path=/Seahub/6.2.x,entries=5],
             SeafFile[repo=01ccc4,path=/Seahub/.DS_Store,size=6148],
             SeafFile[repo=01ccc4,path=/Seahub/error.md,size=127],
             SeafFile[repo=01ccc4,path=/Seahub/preview-research.md,size=1030]]

    print [dirent.name for dirent in lst]
    Out >>> ['6.1.x',
             '6.2.2-pro',
             '6.2.3',
             '6.2.x',
             '.DS_Store',
             'error.md',
             'preview-research.md']
```

**Return Type**

List of SeafDir and SeafFile

### <a id="seafdir_create_empty_file"></a> Create Empty File ###
**Request Parameters**

* name

**Sample Case**

```python

    import seafileapi
	
    client = seafileapi.connect('http://127.0.0.1:8000', 'test@admin.com', 'password')
    repo = client.repos.get_repo('09c16e2a-ff1a-4207-99f3-1351c3f1e507')
    seafdir = repo.get_dir('/root')
	
    new_file = seafdir.create_empty_file('tmp_file.md')
```

**Return Type**

A SeafFile Object of new empty file

### <a id="seafdir_mkdir"></a> Create New Folder ###
**Request Parameters**

* name

**Sample Case**

```python

    import seafileapi
	
    client = seafileapi.connect('http://127.0.0.1:8000', 'test@admin.com', 'password')
    repo = client.repos.get_repo('09c16e2a-ff1a-4207-99f3-1351c3f1e507')
    seafdir = repo.get_dir('/root')
	
    new_dir = seafdir.mkdir('tmp_dir')
```

**Return Type**

A SeafDir Object of new dir

### <a id="seafdir_upload"></a> Upload ###
**Request Parameters**
* fileobj
* filename

**Sample Case**

```python

    import seafileapi
	
    client = seafileapi.connect('http://127.0.0.1:8000', 'test@admin.com', 'password')
    repo = client.repos.get_repo('09c16e2a-ff1a-4207-99f3-1351c3f1e507')
    seafdir = repo.get_dir('/root')
	
    file = seafdir.upload('this is file content', 'tmp_file.md')
```

**Return Type**

A SeafFile Object of upload file


### <a id="seafdir_upload_local_file"></a> Upload Local File ###
**Request Parameters**

* filepath
* name (default None, default use local file name)

**Sample Case**

```python

    import seafileapi
	
    client = seafileapi.connect('http://127.0.0.1:8000', 'test@admin.com', 'password')
    repo = client.repos.get_repo('09c16e2a-ff1a-4207-99f3-1351c3f1e507')
    seafdir = repo.get_dir('/root')
	
    file = seafdir.upload_local_file('/home/ubuntu/env.md')
```

**Return Type**

A SeafFile Object of upload file

**Exception**

* Local file does not exist.

### <a id="seafdir_delete"></a> delete a folder ###
**Request Parameters**

None

**Sample Case**

```python

    import seafileapi
	
    client = seafileapi.connect('http://127.0.0.1:8000', 'test@admin.com', 'password')
    repo = client.repos.get_repo('09c16e2a-ff1a-4207-99f3-1351c3f1e507')
    seafdir = repo.get_dir('/root')
	
    seafdir.delete()
```

**Return Type**

A Response Instance

## <a id="repo"></a> Repo ##
### <a id="repo_from_json"></a> From Json ###
**Request Parameters**

* client
* repo_json

**Sample Case**

```python

    import seafileapi
    from seafileapi.repo import Repo
	
    client = seafileapi.connect('http://127.0.0.1:8000', 'test@admin.com', 'password')
    repo_json = {'id': '09c16e2a-ff1a-4207-99f3-1351c3f1e507', 'name': 'test_repo', 'encrypted': False, 'permission': 'rw', 'owner': 'test@admin.com'}
    repo = Repo.from_json(client, repo_json)
```
	

**Return Type**

A Repo Object

### <a id="repo_is_readonly"></a> Is ReadOnly ###

**Request Parameters**

None

**Sample Case**

```python

    import seafileapi
	
    client = seafileapi.connect('http://127.0.0.1:8000', 'test@admin.com', 'password')
    repo = client.repos.get_repo('09c16e2a-ff1a-4207-99f3-1351c3f1e507')
    is_readonly = repo.is_readonly()
```

**Return Type**

True or False

### <a id="repo_get_file"></a> Get File ###

**Request Parameters**

* path

**Sample Case**

```python

    import seafileapi
	
    client = seafileapi.connect('http://127.0.0.1:8000', 'test@admin.com', 'password')
    repo = client.repos.get_repo('09c16e2a-ff1a-4207-99f3-1351c3f1e507')
    seaffile = repo.get_file('/root/test.md')
```

**Return Type**

A SeafFile Object

**Exception**

* File does not exist.

### <a id="repo_get_dir"></a> Get Dir ###

**Request Parameters**

* path

**Sample Case**

```python

    import seafileapi
	
    client = seafileapi.connect('http://127.0.0.1:8000', 'test@admin.com', 'password')
    repo = client.repos.get_repo('09c16e2a-ff1a-4207-99f3-1351c3f1e507')
    seafdir = repo.get_dir('/root')
```

**Return Type**

A SeafDir Object

**Exception**

* Dir does not exist.

### <a id="repo_delete"></a> Delete Repo ###

**Request Parameters**

None

**Sample Case**

```python

    import seafileapi
	
    client = seafileapi.connect('http://127.0.0.1:8000', 'test@admin.com', 'password')
    repo = client.repos.get_repo('09c16e2a-ff1a-4207-99f3-1351c3f1e507')
    repo.delete()
```

**Return Type**

None


## <a id="repos"></a> Repos ##
### <a id="repos_get_repo"></a> Get Repo ###
**Request Parameters**

* repo_id

**Sample Case**

```python

    import seafileapi
	
    client = seafileapi.connect('http://127.0.0.1:8000', 'test@admin.com', 'password')
    repo = client.repos.get_repo('09c16e2a-ff1a-4207-99f3-1351c3f1e507')
```

**Return Type**

A Repo Object

**Exception**

* Repo does not exist.

### <a id="repos_list_repo"></a> List Repo ###

**Request Parameters**

None

**Sample Case**

```python

    import seafileapi
	
    client = seafileapi.connect('http://127.0.0.1:8000', 'test@admin.com', 'password')
    repo_list = client.repos.list_repos()

    print repo_list
    Out >>> [<seafileapi.repo.Repo at 0x7f1bb0769750>,
             <seafileapi.repo.Repo at 0x7f1bb07693d0>,
             <seafileapi.repo.Repo at 0x7f1bb0769a50>,
             <seafileapi.repo.Repo at 0x7f1bb077cc10>,
             <seafileapi.repo.Repo at 0x7f1bb077cfd0>,
             <seafileapi.repo.Repo at 0x7f1bb077ca10>]

    print [repo.name for repo in repo_list]
    Out >>> ['alphabox',
             'hello',
             'Doc',
             'obj_test',
             'fs_test',
             'global']
```
	

**Return Type**

A list of Repo Object

### <a id="repos_create_repo"></a> Create Repo ###

**Request Parameters**

* name
* password (default None)

**Sample Case**

```python

    import seafileapi
	
    client = seafileapi.connect('http://127.0.0.1:8000', 'test@admin.com', 'password')
    repo = client.repos.create_repo('test_repo')
```

**Return Type**

A Repo Object

