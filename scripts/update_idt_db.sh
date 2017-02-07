#!/bin/bash

BASE_DIR="`dirname \"$0\"`/.."
cd $BASE_DIR

ROOT=`git rev-parse --show-toplevel`
cd ${ROOT}
SRC=${ROOT}/cephia
SITE_PATH=${SRC}
VENV=${ROOT}/venv

echo "activate virtualenv"
cd ${VENV}
. ./bin/activate
if [ $? != 0 ]; then
    echo "failed to activate virtualenv at ${VENV}: ABORTING"
    exit 1
fi
cd -

echo "Running management command update_cephia_infection_dating_tool_tests_and_properties"
cd ${SITE_PATH}
python manage.py update_cephia_infection_dating_tool_tests_and_properties
cd -

echo "Done"
