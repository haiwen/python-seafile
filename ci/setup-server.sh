#!/bin/bash

set -e

# build and run seafile-server
git clone --depth=1 --branch=master git://github.com/haiwen/seafile-test-deploy /tmp/seafile-test-deploy
cd /tmp/seafile-test-deploy
./bootstrap.sh

# run seahub
git clone --depth=1 --branch=master git://github.com/haiwen/seahub /tmp/seahub
cd /tmp/seahub/
pip install -r requirements.txt --allow-all-external --allow-unverified Djblets --allow-unverified PIL
pip install -r test-requirements.txt
cd /tmp/seahub/tests
./seahubtests.sh init
./seahubtests.sh runserver
