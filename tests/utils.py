import string
import random

def randstring(length=12):
    return ''.join(random.choice(string.lowercase) for i in range(length))
