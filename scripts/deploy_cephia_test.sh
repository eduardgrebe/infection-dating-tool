#!/bin/bash

ROOT=`git rev-parse --show-toplevel`
cd ${ROOT}

./scripts/deploy_local.sh

sudo /etc/init.d/apache2 reload

sudo chown -R www-data logs 
sudo chown -R www-data media
sudo chown impd logs/cephia_management.log 

echo "Done"

