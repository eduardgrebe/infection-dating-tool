afrom fabric.api import local, settings, abort, run, cd, env, sudo, lcd
import os
import getpass
import shutil
from fabric.contrib.console import confirm, prompt
from fabric.operations import put
import datetime

local_code_dir = os.path.dirname(os.path.realpath(__file__))
imp_remote_code_staging_dir = "/home/cephia"
cephia_test_remote_code_staging_dir = "/home/cephia/staging"

# ===== Usage =====

usage = """

fonkserver
--------
staging       : > fab host_impd deploy:<branch>
cephia test   : > fab host_cephiatest deploy:<branch>

"""
def help():
    print usage

# ===== hosts ======

def host_impd():
    env.user = 'impd'
    env.hosts = ['cephia.impd.co.za']

def host_cephiatest():
    env.user = 'impd'
    env.hosts = ['cephiatest.eduardgrebe.net']

# ===== top level commands ======

def deploy(branch_name="master"):
    if env.host == 'cephiatest.eduardgrebe.net':
        return _deploy_cephia_test(branch_name)
    elif env.host == 'cephia.impd.co.za':
        return _deploy_staging(branch_name)
    else:
        raise Exception("Unknown host: %s" % env.host)

def _deploy_staging(branch_name="master"):
    print("   Deploying: ** %s **" % branch_name)
    with cd(imp_remote_code_staging_dir):
        run("git reset --hard HEAD")
        run("git fetch origin")
        run("git checkout origin/%s" % branch_name)
        run("git pull origin %s" % branch_name)
        run("./scripts/deploy_impd.sh")
        
    print("Deployed to: http://cephia.impd.co.za/")

def _deploy_cephia_test(branch_name="master"):
    print("   Deploying: ** %s **" % branch_name)
    with cd(cephia_test_remote_code_staging_dir):
        run("git reset --hard HEAD")
        run("git fetch origin %s" % branch_name)
        run("git checkout %s" % branch_name)
        run("git pull origin %s" % branch_name)
        run("./scripts/deploy_cephia_test.sh")
        
    print("Deployed to: http://cephiatest.eduardgrebe.net/")
