#!/bin/bash

BASE_DIR="`dirname \"$0\"`/.."
cd $BASE_DIR

ROOT=`git rev-parse --show-toplevel`
cd ${ROOT}
VENV=${ROOT}/venv

cd ${VENV}
. ./bin/activate
if [ $? != 0 ]; then
    echo "failed to activate virtualenv at ${VENV}: ABORTING"
    exit 1
fi

echo "Running management command update_cephia_infection_dating_tool_tests_and_properties"
cd ${ROOT}

python manage.py update_cephia_infection_dating_tool_tests_and_properties

echo "Done"
