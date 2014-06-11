from fabric import api as fab
import os
from datetime import datetime

APP_DIR = "/srv/www/dashboard.qutm2m.com/"
DATE = datetime.utcnow().strftime("%Y%m%d%H%M%S")

try:
    fab.env.hosts = os.environ['DEPLOY_HOSTS']
except KeyError:
    print "Please set the env variable HOSTS as a comma separated list of hosts to deploy to."

try:
    fab.env.user = os.environ['DEPLOY_USER']
except KeyError:
    print "Please set DEPLOY_USER as a user who has write access to the src directory"


def reload_wsgi():
    with fab.cd(APP_DIR):
        fab.run('touch reload.wsgi')


def deploy():
    with fab.cd(APP_DIR):
        fab.run('wget https://github.com/qutm2m2014/dashboard/archive/master.tar.gz -O %s.tar.gz' % (DATE))
        fab.run('mkdir app/%s' % (DATE))
        fab.run('tar xvf %s.tar.gz -C app/%s --strip-components=1' % (DATE, DATE))
        fab.run('ln -s %sapp/%s %sapp/current' % (APP_DIR, DATE, APP_DIR))
        fab.run('rm %s.tar.gz' % (DATE))
    reload_wsgi()
