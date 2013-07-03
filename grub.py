from fabric.api import *

@task
def update_grub():
    with settings(parallel=True):
        run("update-grub")

@task
def set_recordfail_timeout():
    with settings(parallel=True):
        run("echo 'GRUB_RECORDFAIL_TIMEOUT=5' >> /etc/default/grub")