# Quick start of Seafile Python SDK

Seafile Python SDK provides functions to read and write files in Seafile server.

## Setups

```basic
pip install seafileapi2
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
from seafileapi2 import SeafileAPI
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
from seafileapi2 import SeafileAPI
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
from seafileapi2 import SeafileAPI
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

Sample results:

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

Parameters

* repo_name: 
* passwd: ou can assign a password to a library to protect it.

**Example** :

```python
seafile_api.create_repo("My new repo")
```

And then a repo object returned as:

```python
<seafileapi.main.Repo object at 0x7f9417360fa0>
```



### Delete repo

```python
seafile_api.delete_repo(repo_id)
```

**Example:**

```python
repo_id = "83066b00-67ef-4068-b738-7a7381558d1b"
seafile_api.delete_repo(repo_id)
```



## File / Dir operation

In the previous section, we talked about how to authorize a repo, and once authorized, you can manipulate the files and directories inside based on the functions in repo object. 

### List dir

List the items inside a specific directory of a path

```python
repo.list_dir(dir_path = '/')
```

**Example:**

```python
repo.list_dir('/root')
```

And then the items returned as:

```
[{
	'type': 'dir',
	'id': '431b66c52e4865d7757fca76fb358f8eb3e7e8d5',
	'name': 'auto-upload',
	'mtime': '2023-03-14T14:36:49+08:00',
	'permission': 'rw',
	'parent_dir': '/images/',
	'starred': False
}, {
	'type': 'file',
	'id': '9669d47f26f709148e1b36917a90b9eecb167167',
	'name': '6613.txt',
	'mtime': '2020-12-26T10:14:52+08:00',
	'permission': 'rw',
	'parent_dir': '/images/',
	'size': 14,
	'modifier_email': 'jiwei.ran@seafile.com',
	'modifier_name': '冉继伟',
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



### Create a dir

```python
repo.create_dir(path)
```

* path, the directory you want to create

**Example:**

```python
repo.create_dir('/A new')
```

And then the result returned as:

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



### Rename a dir

```python
repo.rename_dir(path, new_name)
```

**Example:**

```python
repo.rename_dir('/A new', 'new file')
```

And then the result returned as:

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



### Delete dir

```python
repo.delete_dir(path)
```

**Example:**

```python
repo.delete_dir('/new file')
```



### Get a file

Get details of a file

```python
repo.get_file(path)
```

**Example**

```python
repo.get_file('/file/readme.txt')
```

And then the result returned as:

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

**Example**

```python
repo.create('/file/d.txt')
```

And then the result returned as:

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

**Example**

```python
repo.rename_file('/file/readme.txt', 'readme1.txt')
```

And then the result returned as:

```
{
	'type': 'file',
	'repo_id': '83066b00-67ef-4068-b738-7a7381558d1b',
	'parent_dir': '/images',
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

**Example**

```python
repo.delete_file('/file/readme.txt')
```



### Get repo details

```python
repo.get_repo_details()
```

And then the result returned as:

```
{
	'repo_id': '83066b00-67ef-4068-b738-7a7381558d1b',
	'repo_name': 'My files',
	'size': 44219022,
	'file_count': 126,
	'last_modified': '2024-04-12T12:35:42+08:00'
}
```





