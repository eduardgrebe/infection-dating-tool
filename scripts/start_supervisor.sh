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

echo "Restarting supervisor process"
cd ${ROOT}

supervisord -c supervisord.conf -d .
supervisorctl stop all
supervisorctl reread
supervisorctl start all

