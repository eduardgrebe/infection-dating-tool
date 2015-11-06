 #!/bin/bash
BASE_DIR="`dirname \"$0\"`/.."
cd $BASE_DIR

ROOT=$(pwd)

LOG_DIR=${ROOT}/logs
PID_FILE=${LOG_DIR}/run_commands.pid

if [ -f ${PID_FILE} ]; then
    echo "Already running, delete ${PID_FILE} to restart"
    exit 1
fi
touch ${PID_FILE}


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
python manage.py import_pending_files --settings=cephia.management_settings
python manage.py validate_imported_files --settings=cephia.management_settings
python manage.py process_validated_files --settings=cephia.management_settings
python manage.py validate_imported_files_2 --settings=cephia.management_settings
python manage.py process_validated_files_2 --settings=cephia.management_settings
python manage.py associate_subject_visit --settings=cephia.management_settings
python manage.py associate_specimen_visit --settings=cephia.management_settings

rm -f ${PID_FILE}
