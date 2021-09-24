import string
import random
from functools import wraps
from urllib.parse import urlencode
from seafileapi.exceptions import ClientHttpError, DoesNotExist

def randstring(length=0):
    if length == 0:
        length = random.randint(1, 30)
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

def urljoin(base, *args):
    url = base
    if url[-1] != '/':
        url += '/'
    for arg in args:
        arg = arg.strip('/')
        url += arg + '/'
    if '?' in url:
        url = url[:-1]
    return url

def raise_does_not_exist(msg):
    """Decorator to turn a function that get a http 404 response to a
    :exc:`DoesNotExist` exception."""
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ClientHttpError as e:
                if e.code == 404:
                    raise DoesNotExist(msg)
                else:
                    raise
        return wrapped
    return decorator

def to_utf8(obj):
    if isinstance(obj, str):
        return obj.encode('utf-8')
    return obj

def querystr(**kwargs):
    return '?' + urlencode(kwargs)

def utf8lize(obj):
    if isinstance(obj, dict):
        return {k: to_utf8(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [to_utf8(x) for x in obj]

    if isinstance(obj, str):
        return obj.encode('utf-8')

    return obj
