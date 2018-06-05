# Python Seafile
<p><div class="doc">
<ul>
<li><a href="#get_client">Get Client</a></li>
<li>
	<a href="#repo"> Library </a>
	<ul>
		<li><a href="#repo_get_repo">Get Library</a></li>
		<li><a href="#repo_is_readonly">Check Library Permission</a></li>
		<li><a href="#repo_list_repo">List all Libraries</a></li>
		<li><a href="#repo_create_repo">Create Library</a></li>
		<li><a href="#repo_delete">Delete Library</a></li>
	</ul>
</li>
<li>
	<a href="#seafdir">Directory</a>
	<ul>
		<li><a href="#seafdir_get">Get Directory</a></li>
		<li><a href="#seafdir_ls">List Directory Entries</a></li>
		<li><a href="#seafdir_mkdir">Create New Folder</a></li>
		<li><a href="#seafdir_delete">Delete Directory</a></li>
	</ul>
</li>
<li>
	<a href="#seaffile">File</a>
	<ul>
		<li><a href="#seaffile_get">Get File</a></li>
		<li><a href="#seaffile_get_content">Get Content</a></li>
		<li><a href="#seaffile_create_empty_file">Create Empty File</a></li>
		<li><a href="#seaffile_upload">Upload File</a></li>
		<li><a href="#seaffile_delete">Delete file</a></li>
	</ul>
</li>
<li>
	<a href="#user">User</a>
	<ul>
		<li><a href="#user_get_accounts">Get accounts</a></li>
		<li><a href="#user_create_account">Create account</a></li>
		<li><a href="#user_delete_account">Delete account</a></li>
		<li><a href="#user_add_account_to_group">Add account to group</a></li>
	</ul>
</li>
<li>
	<a href="#group">Group</a>
	<ul>
		<li><a href="#group_get_groupss">Get groups</a></li>
		<li><a href="#group_create_group">Create group</a></li>
		<li><a href="#group_delete_group">Delete group</a></li>
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


## <a id="repo"></a> Library ##
### <a id="repo_get_repo"></a> Get Library ###
**Request Parameters**

* repo_id

**Sample Case**

```python

    import seafileapi
	
    client = seafileapi.connect('http://127.0.0.1:8000', 'test@admin.com', 'password')
    repo = client.repos.get_repo('09c16e2a-ff1a-4207-99f3-1351c3f1e507')
```

**Return Type**

A Library Object

**Exception**

* Library does not exist.

### <a id="repo_is_readonly"></a> Check Library Permission ###

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

Boolean

### <a id="repo_list_repo"></a> List all Libraries ###

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

A list of Libraries Object

### <a id="repo_create_repo"></a> Create Library ###

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

A Library Object


### <a id="repo_delete"></a> Delete Library ###

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

## <a id="seafdir"></a> Directory ##
### <a id="seafdir_get"></a> Get Directory ###

**Request Parameters**

* path

**Sample Case**

```python

    import seafileapi
	
    client = seafileapi.connect('http://127.0.0.1:8000', 'test@admin.com', 'password')
    repo = client.repos.get_repo('09c16e2a-ff1a-4207-99f3-1351c3f1e507')
    seafdir = repo.get_dir('/root')
    print seafdir.__dict__
    Out >>> {'client': SeafileApiClient[server=http://127.0.0.1:8000, user=admin@admin.com],
             'entries': [],
             'id': 'c3742dd86004d51c358845fa3178c87e4ab3aa60',
             'path': '/root',
             'repo': <seafileapi.repo.Repo at 0x7f2af56b1490>,
             'size': 0}
```

**Return Type**

A Directory Object

**Exception**

* Directory does not exist.

### <a id="seafdir_ls"></a> List Directory Entries ###
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

List of Directory and File


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

A Directory Object of new directory

### <a id="seafdir_delete"></a> Delete Directory ###
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


## <a id="seaffile"></a> File ##
### <a id="seaffile_get"></a> Get File ###

**Request Parameters**

* path

**Sample Case**

```python

    import seafileapi
	
    client = seafileapi.connect('http://127.0.0.1:8000', 'test@admin.com', 'password')
    repo = client.repos.get_repo('09c16e2a-ff1a-4207-99f3-1351c3f1e507')
    seaffile = repo.get_file('/root/test.md')

    print seafile.__dict__
    Out >>> {'client': SeafileApiClient[server=http://127.0.0.1:8000, user=admin@admin.com],
             'id': '0000000000000000000000000000000000000000',
             'path': '/root/test.md',
             'repo': <seafileapi.repo.Repo at 0x7f2af56b1490>,
             'size': 0}
```

**Return Type**

A File Object

**Exception**

* File does not exist.

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

### <a id="seaffile_create_empty_file"></a> Create Empty File ###
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

A File Object of new empty file


### <a id="seaffile_upload_file"></a> Upload File ###
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

A File Object of upload file

**Exception**

* Local file does not exist.


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


## <a id="user"></a> User ##

### <a id="user_get_accounts"></a> Get accounts ###
**Request Parameters**

None

**Sample Case**

```python

    import seafileapi
	
    client = seafileapi.connect('http://127.0.0.1:8000', 'test@admin.com', 'password')
    accounts = client.users.get_accounts()
```

**Return Type**

A list of dictionnary containing source and email keys.

**Exception**

TBD

### <a id="user_create_account"></a> Create account ###
**Request Parameters**

* email -- email as login name
* password -- plain text password
* name -- full text display name
* groups_names -- list of groups' names to add this user to
* note -- description / comment / whatever
* is_staff -- is admin, default False
* is_active -- can connect, default True


**Sample Case**

```python

    import seafileapi
	
    client = seafileapi.connect('http://127.0.0.1:8000', 'test@admin.com', 'password')
    accounts = client.users.create_account('test@admin.com', 'password', 'Test user', ['admins'])
```

**Return Type**

A dictionnary, containing the created user.

**Exception**

TBD


### <a id="user_delete_account"></a> Delete account ###
**Request Parameters**

* email -- email as login name


**Sample Case**

```python

    import seafileapi
	
    client = seafileapi.connect('http://127.0.0.1:8000', 'test@admin.com', 'password')
    accounts = client.users.delete_account('test@admin.com')
```

**Return Type**

TBD

**Exception**

TBD


### <a id="user_add_account_to_group"></a> Add account to group ###
**Request Parameters**

* username -- email as login name
* groups_name -- group's name to add this user to

**Sample Case**

```python

    import seafileapi
	
    client = seafileapi.connect('http://127.0.0.1:8000', 'test@admin.com', 'password')
    accounts = client.users.add_account_to_group('test@admin.com', 'admins')
```

**Return Type**

TBD

**Exception**

TBD




## <a id="group"></a> Group ##

### <a id="group_get_groups"></a> Get groups ###
**Request Parameters**

None

**Sample Case**

```python

    import seafileapi
	
    client = seafileapi.connect('http://127.0.0.1:8000', 'test@admin.com', 'password')
    groups = client.groups.get_groups()
```

**Return Type**

A list of groups.

**Exception**

TBD



### <a id="group_create_group"></a> Create group ###
**Request Parameters**

* group_name -- group's name


**Sample Case**

```python

    import seafileapi
	
    client = seafileapi.connect('http://127.0.0.1:8000', 'test@admin.com', 'password')
    accounts = client.groups.create_group('admins')
```

**Return Type**

TBD

**Exception**

TBD


### <a id="group_delete_group"></a> Delete group ###
**Request Parameters**

* group_name -- group's name


**Sample Case**

```python

    import seafileapi
	
    client = seafileapi.connect('http://127.0.0.1:8000', 'test@admin.com', 'password')
    accounts = client.groups.delete_group('admin')
```

**Return Type**

TBD

**Exception**

TBD

