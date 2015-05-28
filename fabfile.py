from fabric.api import local, settings, abort, run, cd, env, sudo, lcd
import os
import getpass
import shutil
from fabric.contrib.console import confirm, prompt
from fabric.operations import put
import datetime

local_code_dir = os.path.dirname(os.path.realpath(__file__))
imp_remote_code_staging_dir = "/home/cephia"

# ===== Usage =====

usage = """

fonkserver
--------
staging       : > fab host_impd deploy_staging:<branch>

"""
def help():
    print usage

# ===== hosts ======

def host_impd():
    env.user = 'impd'
    env.hosts = ['cephia.impd.co.za']

# ===== top level commands ======

def deploy_staging(branch_name="master"):

    print("   Deploying: ** %s **" % branch_name)

    with cd(imp_remote_code_staging_dir):
        run("git reset --hard HEAD")
        run("git checkout %s" % branch_name)
        run("git pull origin %s" % branch_name)
        run("./scripts/deploy_impd.sh")
        
    print("Deployed to: http://cephia.impd.co.za/")
