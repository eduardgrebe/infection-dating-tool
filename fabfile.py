from fabric.api import run, cd, env
import os
from cephia.lib.fab_deploy_cron import crontab_update, crontab_remove_all_with_marker

local_code_dir = os.path.dirname(os.path.realpath(__file__))
imp_remote_code_staging_dir = "/home/cephia"
cephia_test_remote_code_staging_dir = "/home/cephia/cephia"
cephia_prod_remote_code_prod_dir = "/home/cephia/cephia_prod"

# ===== Usage =====

usage = """


--------
staging       : > fab host_impd deploy:<branch>
cephia test   : > fab host_cephia_test deploy:<branch>
cephia prod   : > fab host_cephia_prod deploy:<branch>

"""
def help():
    print usage

# ===== hosts ======

def host_impd():
    env.user = 'impd'
    env.hosts = ['cephia.impd.co.za']

def host_cephia_test():
    env.user = 'cephia'
    env.hosts = ['cephiadb2.incidence-estimation.org']

def host_cephia_prod():
    env.user = 'cephia'
    env.hosts = ['cephiadb.incidence-estimation.org']

# ===== top level commands ======

def deploy(branch_name="master"):
    if env.host == 'cephiadb2.incidence-estimation.org':
        return _deploy_cephia_test(branch_name)
    elif env.host == 'cephiadb.incidence-estimation.org':
        return _deploy_cephia_prod(branch_name)
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
        
    _update_cron_jobs()
    
    print("Deployed to: http://cephiadb2.incidence-estimation.org/")

def _deploy_cephia_prod(branch_name="master"):
    print("   Deploying: ** %s **" % branch_name)
    with cd(cephia_prod_remote_code_prod_dir):
        run("git reset --hard HEAD")
        run("git fetch origin %s" % branch_name)
        run("git checkout %s" % branch_name)
        run("git pull origin %s" % branch_name)
        run("./scripts/deploy_cephia_prod.sh")
        
    _update_cron_jobs()
    
    print("Deployed to: http://cephiadb.incidence-estimation.org/")

def _update_cron_jobs():

    def create_cron_line(script_name, stars, marker_tag="CEPHIATEST"):
        crontab_remove_all_with_marker(marker_tag="CEPHIATEST")
        crontab_update("{stars} /home/cephia/cephia/scripts/{script_name}.sh > /home/cephia/cephia/logs/{script_name}.log 2>&1".format(stars=stars,script_name=script_name),
                       marker=marker_tag)

    def create_cron_line_prod(script_name, stars, marker_tag="CEPHIAPROD"):
        crontab_remove_all_with_marker(marker_tag="CEPHIAPROD")
        crontab_update("{stars} /home/cephia/cephia_prod/scripts/{script_name}.sh > /home/cephia/cephia_prod/logs/{script_name}.log 2>&1".format(stars=stars,script_name=script_name),
                       marker=marker_tag)
        
    ## Every minute
    create_cron_line(script_name='run_commands', stars="* * * * *")
    create_cron_line_prod(script_name='run_commands', stars="* * * * *")
