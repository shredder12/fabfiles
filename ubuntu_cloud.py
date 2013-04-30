from fabric.api import *

def check_ubuntu_cloud_repo():
    run("ls -l /etc/apt/sources.list.d/ubuntu-cloud.list")

@task
def add_ubuntu_cloud_repo():
    run("echo 'deb http://ubuntu-cloud.archive.canonical.com/ubuntu \
            precise-updates/folsom main' > /etc/apt/sources.list.d/ubuntu-cloud.list")

@task
def add_ubuntu_cloud_keyring():
    run("apt-get install -y ubuntu-cloud-keyring")
