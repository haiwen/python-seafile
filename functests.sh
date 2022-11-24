#!/bin/bash

: ${PYTHON=python}

: ${SEAFILE_TEST_SERVER_ADDRESS="http://127.0.0.1:8000"}
: ${SEAFILE_TEST_USERNAME="test@example.com"}
: ${SEAFILE_TEST_PASSWORD="testtest"}
: ${SEAFILE_TEST_ADMIN_USERNAME="admin@example.com"}
: ${SEAFILE_TEST_ADMIN_PASSWORD="adminadmin"}

export SEAFILE_TEST_SERVER_ADDRESS
export SEAFILE_TEST_USERNAME
export SEAFILE_TEST_PASSWORD
export SEAFILE_TEST_ADMIN_USERNAME
export SEAFILE_TEST_ADMIN_PASSWORD

SCRIPT=$(readlink -f "$0")
SRCDIR=$(dirname "${SCRIPT}")

cd "${SRCDIR}"

py.test $@
