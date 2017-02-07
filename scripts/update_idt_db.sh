#!/bin/bash

BASE_DIR="`dirname \"$0\"`/.."
cd $BASE_DIR

ROOT=`git rev-parse --show-toplevel`
cd ${ROOT}
SRC=${ROOT}/cephia
SITE_PATH=${SRC}

echo "Running management command update_cephia_infection_dating_tool_tests_and_properties"
cd ${SITE_PATH}
python manage.py update_cephia_infection_dating_tool_tests_and_properties  --noinput --verbosity=0 --settings=cephia.management_settings
cd -

echo "Done"
