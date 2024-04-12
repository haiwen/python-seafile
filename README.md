# Quick start of Seafile Python SDK 2.0

Seafile Python SDK provides functions to read and write files in Seafile server.

## Setups

```basic
pip install seafileapi
```


## Basic objects

Two basic objects are used in Seafile Python SDK.

#### SeafileAPI

You can initialize a SeafileAPI object with user's login name and password.  After authentication, you can get library objects for specific libraries to manipulate on libraries.

#### Repo

A repo object represents a library in Seafile. You can use it to manipulate files and folders inside a library.

> Hints: In Seafile project, "Repo" is the short for "Repository". It has a same meaning of the term "library".


## SeafileAPI authentication

SeafileAPI object can be authenticated by using user's username and password.

```
from seafileapi import SeafileAPI
server_url = "https://cloud.seafile.com/"
login_name = "example@examle.com"
pwd = "password"
seafile_api = SeafileAPI(login_name, pwd, server_url)
seafile_api.auth()
```

## Repo authentication

There are two ways to get an authenticated repo object:

#### By username and password

```python
from seafileapi import SeafileAPI
server_url = "https://cloud.seafile.com/"
login_name = "example@examle.com"
pwd = "password"
seafile_api = SeafileAPI(login_name, pwd, server_url)
seafile_api.auth()
repo_id = "xxxxxxxxxxxx"
repo = seafile_api.get_repo(repo_id) # return <Repo> object
```

#### By Repo API-Token

You can generate API-Token for a repo in Seafile Web interface (In the "Advanced" --> "API Token" in the dropdown menu of a library). Every API-Token can have different read or write permissions. This token is valid until you delete them.

```python
from seafileapi import SeafileAPI
server_url = "https://cloud.seafile.com/"
api_token = '6de40d8456b06bdb4c9eabbf658175bdc4084050'
api_repo = Repo(api_token, server_url)
api_repo.auth()
```

## Repo operations 

You can use SeafileAPI object to list/add/delete repos.

### List repos

```python
seafile_api.list_repos()
```

Return the list of repos accessible by the current user.

**Example**

```python
seafile_api.list_repos()
```

A list of repos in plain objects is returned:

```
[
    {
	'type': 'repo',
	'id': '83066b00-67ef-4068-b738-7a7381558d1b',
	'owner': 'jiwei.ran@seafile.com',
	'owner_name': 'Jiwei',
	'owner_contact_email': 'r350178982@126.com',
	'name': 'My files',
	'mtime': 1712741554,
	'modifier_email': 'jiwei.ran@seafile.com',
	'modifier_contact_email': 'r350178982@126.com',
	'modifier_name': 'Jim',
	'mtime_relative': '<time datetime="2024-04-10T17:32:34" is="relative-time" title="Wed, 10 Apr 2024 17:32:34 +0800" >1 day ago</time>',
	'size': 44219022,
	'size_formatted': '42.2\xa0MB',
	'encrypted': False,
	'permission': 'rw',
	'virtual': False,
	'root': '',
	'head_commit_id': 'e27451a9c3e4a9f558bc15eacbf9e33a7b3f3ab5',
	'version': 1,
	'salt': ''
    },
    .....
]
```


### Create repo

```python
seafile_api.create_repo(repo_name, passwd=None)
```

Create a repo and return the repo object.

**Parameters**:

* repo_name: the name of the library.
* passwd: if specified, an encrypted library is created.

**Example**

```python
seafile_api.create_repo("My new repo")
```

The newly created repo object is returned:

```python
<seafileapi.main.Repo object at 0x7f9417360fa0>
```


### Delete repo

```python
seafile_api.delete_repo(repo_id)
```

**Parameters:**

* repo_id: unique identifier of a library

**Example:**

```python
repo_id = "83066b00-67ef-4068-b738-7a7381558d1b"
seafile_api.delete_repo(repo_id)
```



## File / folder operation

You can use Repo object to manipulate files and folders.

### List folder items

```python
repo.list_dir(dir_path = '/')
```

Return the list of items in plain objects showed in a specific folder.

**Example:**

```python
repo.list_dir('/root') 
```

A list of folder items in plain objects is returned:

```
[{
	'type': 'dir',
	'id': '431b66c52e4865d7757fca76fb358f8eb3e7e8d5',
	'name': 'auto-upload',
	'mtime': '2023-03-14T14:36:49+08:00',
	'permission': 'rw',
	'parent_dir': '/root',
	'starred': False
}, {
	'type': 'file',
	'id': '9669d47f26f709148e1b36917a90b9eecb167167',
	'name': '6613.txt',
	'mtime': '2020-12-26T10:14:52+08:00',
	'permission': 'rw',
	'parent_dir': '/root',
	'size': 14,
	'modifier_email': 'jiwei.ran@seafile.com',
	'modifier_name': 'Jiwei',
	'modifier_contact_email': 'r350178982@126.com',
	'is_locked': False,
	'lock_time': 0,
	'lock_owner': '',
	'lock_owner_name': '',
	'lock_owner_contact_email': '',
	'locked_by_me': False,
	'starred': False
}, ...]
```

### Create a folder

```python
repo.create_dir(path)
```

Create a folder and return a plain object.

**Example:**

```python
repo.create_dir('/A new')
```

A folder in plain object is returned

```
{
	'type': 'dir',
	'repo_id': '83066b00-67ef-4068-b738-7a7381558d1b',
	'parent_dir': '/',
	'obj_name': 'A new',
	'obj_id': '0000000000000000000000000000000000000000',
	'mtime': '2024-04-12T12:18:18+08:00'
}
```

### Rename a folder

```python
repo.rename_dir(path, new_name)
```

Change the folder name and return a plain object.

**Example:**

```python
repo.rename_dir('/A new', 'new file')
```

A folder in plain object is returned:

```
{
	'type': 'dir',
	'repo_id': '83066b00-67ef-4068-b738-7a7381558d1b',
	'parent_dir': '/',
	'obj_name': 'new file',
	'obj_id': '0000000000000000000000000000000000000000',
	'mtime': '2024-04-12T12:18:18+08:00'
}
```

### Delete a folder

```python
repo.delete_dir(path)
```

A folder in a specific path will be deleted.

**Example:**

```python
repo.delete_dir('/new file')
```



### Get a file

```python
repo.get_file(path)
```

Get details of a file and return a plain object

**Example**

```python
repo.get_file('/file/readme.txt')
```

A file in plain object is returned:

```
{
	'type': 'file',
	'repo_id': '83066b00-67ef-4068-b738-7a7381558d1b',
	'parent_dir': '/file',
	'obj_name': '7713.txt',
	'obj_id': 'f8da2b1f7562988bf7bc9b9760a1a4b687d897b2',
	'size': 14,
	'mtime': '2020-12-26T10:14:52+08:00',
	'can_preview': True,
	'can_edit': True
}
```

### Create a file

```python
repo.create_file(path)
```

Create a file and return a plain object.

**Example**

```python
repo.create('/file/d.txt')
```

A file in plain object is returned:

```
{
	'type': 'file',
	'repo_id': '83066b00-67ef-4068-b738-7a7381558d1b',
	'parent_dir': '/file',
	'obj_name': d.txt',
	'obj_id': '9484a2b1f756381b9760a1a4b687d897b2',
	'size': 12,
	'mtime': '2020-12-26T10:14:52+08:00',
	'can_preview': True,
	'can_edit': True
}
```

### Rename a file

```python
repo.rename_file(path, new_name)
```

Change the file  name and return a plain object.

**Parameters:**

* path: a path with old file name.

**Example**

```python
repo.rename_file('/file/readme.txt', 'readme1.txt')
```

A file in plain object is returned:

```
{
	'type': 'file',
	'repo_id': '83066b00-67ef-4068-b738-7a7381558d1b',
	'parent_dir': '/file',
	'obj_name': 'readme1.txt',
	'obj_id': '0000000000000000000000000000000000000000',
	'size': 0,
	'mtime': '2024-04-12T12:32:26+08:00',
	'can_preview': True,
	'can_edit': True
}
```

### Delete a file

```python
repo.delete_file(path)
```

A file in a specific path will be deleted.

**Example**

```python
repo.delete_file('/file/readme.txt')
```

### Get repo details

```python
repo.get_repo_details()
```

A repo info in plain object is returned:

```
{
	'repo_id': '83066b00-67ef-4068-b738-7a7381558d1b',
	'repo_name': 'My files',
	'size': 44219022,
	'file_count': 126,
	'last_modified': '2024-04-12T12:35:42+08:00'
}
```





