from fabric.api import *

passwd="4jkl2bh3"

def create_ceph_user():
    with settings(disable_known_hosts=True, warn_only=True):
        run("useradd -d /home/ceph -m ceph")
        run("echo 'ceph:" + passwd + "' | chpasswd")

def sudo_ceph():
    run("echo 'ceph ALL = (root) NOPASSWD:ALL' | tee /etc/sudoers.d/ceph")

@task
def setup_ceph_server():
    create_ceph_user()
    sudo_ceph()