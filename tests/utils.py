import os
import string
import random

def randstring(length=12):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

def datafile(filename):
    return os.path.join(os.path.dirname(__file__), 'data', filename)

def filesize(path):
    return os.stat(path).st_size
