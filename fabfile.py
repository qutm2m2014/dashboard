from fabric import api as fab
import os
from datetime import datetime
from ftplib import FTP
from fabric.colors import *
from subprocess import call

APP_DIR = "/srv/www/dashboard.qutm2m.com/"
DATE = datetime.utcnow().strftime("%Y%m%d%H%M%S")

APP_NAME = 'manager.qutm2m.com'

FTP_SERVER = '203.42.134.70'
FTP_USERNAME = 'QUT'
FTP_PASSWORD = 'GmRXEy3p'
FTP_SUB_DIR = '/submission/code'

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
        fab.run('rm -rf %s/app/current', (APP_DIR))
        fab.run('ln -s %sapp/%s %sapp/current' % (APP_DIR, DATE, APP_DIR))
        fab.run('rm %s.tar.gz' % (DATE))
    reload_wsgi()


@fab.task
def zip():
    filename = '%s-%s.zip' % (APP_NAME, DATE)
    command = 'zip -q -x "*.pyc" -x "*.DS_Store" -x "**/node_modules**" -x "**/static/libs**" -x "*.git*" -r %s ./' % (filename)
    call(command, shell=True)
    return filename


def _connectToFTP():
    ftp = FTP(host=FTP_SERVER)
    ftp.login(user=FTP_USERNAME, passwd=FTP_PASSWORD)
    ftp.cwd(FTP_SUB_DIR)
    return ftp


@fab.task
def testftp():
    ftp = _connectToFTP()
    print cyan(FTP.getwelcome(ftp))
    print cyan(ftp.pwd())
    ftp.quit()


@fab.task
def deployToFTP():
    print cyan("Creating zip of code")
    zipf = zip()
    print cyan("Connecting to FTP Server")
    ftp = _connectToFTP()
    f = open(zipf, 'rb')
    print cyan("Uploading...", os.path.join(FTP_SUB_DIR, zipf))
    ftp.storbinary("STOR %s" % zipf, f)
    ftp.close()
    print cyan("Removing Temporary zip file")
    os.remove(zipf)
