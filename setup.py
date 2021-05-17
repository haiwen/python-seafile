from setuptools import setup, find_packages
import re


def get_version():
    #https://stackoverflow.com/a/7071358/5122790
    VERSIONFILE="python_seafile/_version.py"
    verstrline = open(VERSIONFILE, "rt").read()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        return mo.group(1)
    else:
        raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))


setup(name='python_seafile',
      version=get_version(),
      license='BSD',
      description='Client interface for Seafile Web API',
      author='Shuai Lin',
      author_email='linshuai2012@gmail.com, cstenkamp@uos.de',
      url='http://seafile.com',
      platforms=['Any'],
      packages=find_packages(),
      install_requires=['requests', 'requests-toolbelt'],
      classifiers=['Development Status :: 4 - Beta',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python 3'],
      )
