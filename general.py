from fabric.api import *

@task
def check_update():
    run("apt-get update")

@task
def upgrade():
    check_update()
    run("apt-get -y upgrade")

@task
def hostname():
    run("hostname")