# Upload to pypi

1. first update version and check `install_requires` in `setup.py`
2. python3 setup.py check
3. python3 setup.py sdist build
4. python3 setup.py bdist_wheel
5. twine upload dist/*
