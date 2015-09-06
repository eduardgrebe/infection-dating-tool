 #!/bin/bash

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

cd ${SITE_PATH}
python manage.py associate_subject_visit --settings=cephia.management_settings
