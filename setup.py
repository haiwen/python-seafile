from setuptools import setup, find_packages

__version__ = '0.1.1'


setup(
    name='seafileapi',
    version=__version__,
    license='BSD',
    description='Python client for Seafile Web API',
    author='seafile',
    author_email='support@seafile.com',
    url='https://github.com/haiwen/python-seafile',
    platforms='any',
    packages=find_packages(),
    install_requires=['requests'],
    classifiers=['Programming Language :: Python'],
)
