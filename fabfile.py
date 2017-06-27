from __future__ import with_statement
import os
from fabric.api import *

# ===== Usage =====

usage = """


--------
staging       : > fab host_impd deploy:<branch>
cephia test   : > fab host_cephia_test deploy:<branch>
cephia prod   : > fab host_cephia_prod deploy:<branch>
idt prod      : > fab host_idt_prod deploy:<branch>

shiny         : > fab host_shiny_prod deploy_shiny:<branch>
shiny server  : > fab host_shiny_prod restart_shiny_server

"""

def help():
    print usage

# ===== hosts ======

def host_impd():
    env.user = 'impd'
    env.hosts = ['cephia.impd.co.za']
    env.code_dir = '/home/cephia'

def host_cephia_test():
    env.user = 'cephia'
    env.hosts = ['cephiadb2.incidence-estimation.org']
    env.code_dir = "/home/cephia/cephia"

def host_cephia_prod():
    env.user = 'cephia'
    env.hosts = ['cephiadb.incidence-estimation.org']
    env.code_dir = "/home/cephia/cephia_prod"

def host_idt_prod():
    env.user = 'cephia'
    env.hosts = ['tools.incidence-estimation.org']
    env.code_dir = "/home/cephia/idt_prod"

# ===== top level commands ======

def deploy(branch_name="master"):
    print("   Deploying: ** %s **" % branch_name)
    with cd(env.code_dir):
        run("git reset --hard HEAD")
        run("git fetch origin")
        run("git checkout origin/%s" % branch_name)
        run("git pull origin %s" % branch_name)
        run("./scripts/deploy_server.sh")
        run("chmod +x ./scripts/update_idt_db.sh")
        run("./scripts/update_idt_db.sh")

    print("Deployed to: %s" % env.hosts[0])

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


# From http://django-fab-deploy.readthedocs.org/en/0.7.5/_modules/fab_deploy/crontab.html#crontab_update
MARKER_TAG="CEPHIAMARKER"

def _marker(marker):
    return ' # %s:%s' % (MARKER_TAG,marker) if marker else ''

def _get_current():
    with settings(hide('warnings', 'stdout'), warn_only=True):
        output = run('crontab -l')
        return output if output.succeeded else ''

def crontab_set(content):
    """ Sets crontab content """
    run("echo '%s' | crontab -" % content)

def crontab_show():
    """ Shows current crontab """
    puts(_get_current())

def crontab_add(content, marker=None):
    """ Adds line to crontab. Line can be appended with special marker comment so it'll be possible to reliably remove or update it later. """
    old_crontab = _get_current()
    crontab_set(old_crontab + '\n' + content + _marker(marker))

def crontab_remove_all_with_marker(marker_tag=None):
    lines = [line for line in _get_current().splitlines() if marker_tag not in line]
    crontab_set("\n".join(lines))
    
def crontab_remove(marker):
    """ Removes a line added and marked using crontab_add. """
    lines = [line for line in _get_current().splitlines() if line and not line.endswith(marker)]
    crontab_set("\n".join(lines))

def crontab_update(content, marker):
    """ Adds or updates a line in crontab. """
    crontab_remove(marker)
    crontab_add(content, marker)

# ===== shiny app commands ======

def host_shiny_prod():
    env.user = 'cephia'
    env.hosts = ['cephiadb.incidence-estimation.org']
    env.code_dir = "~/shiny-inctools"

def deploy_shiny(branch_name="master"):
    print("   Deploying: ** %s **" % branch_name)
    with cd(env.code_dir):
        run("git reset --hard HEAD")
        run("git fetch origin")
        run("git checkout origin/%s" % branch_name)
        run("git pull origin %s" % branch_name)
        run("sudo service shiny-server restart")

    print("Deployed to: %s" % env.hosts[0])
