from fabric.api import run, env, roles, settings, cd
from roles import roles_dict

env.user = "root"
env.roledefs = roles_dict

def check_update():
    run("apt-get update")

def check_ubuntu_cloud_repo():
    run("ls -l /etc/apt/sources.list.d")

def swift_all_start():
    with settings(parallel=True):
        run("swift-init all start")

def swift_all_stop():
    with settings(parallel=True, warn_only=True):
        run("swift-init all stop")

def swift_proxy_start():
    run("swift-init proxy start")

def swift_proxy_stop():
    run("swift-init proxy stop")

def swift_rest_start():
    run("swift-init rest start")

def swift_rest_stop():
    run("swift-init rest stop")

def hostname():
    run("hostname")

@roles('swift_proxy')
def copy_ring_files():
    for node in env.roledefs['swift_nodes_public']:
        run('scp /etc/swift/*.ring.gz root@{0}:/etc/swift'.format(node))

@roles('swift_proxy')
def add_nodes_to_ring():
    with cd('/etc/swift'):
        for node in env.roledefs['swift_nodes_private']:
            run('swift-ring-builder account.builder add z1-{0}:6002/sdb1 2000'.format(node))
            run('swift-ring-builder container.builder add z1-{0}:6001/sdb1 2000'.format(node))
            run('swift-ring-builder object.builder add z1-{0}:6000/sdb1 2000'.format(node))

@roles('swift_proxy')
def ring_rebalance():
    with cd('/etc/swift'):
        run('swift-ring-builder account.builder rebalance')
        run('swift-ring-builder container.builder rebalance')
        run('swift-ring-builder object.builder rebalance')

def delete_data():
    with settings(parallel=True):
        run("umount /srv/node/sdb1")
        run("mkfs.xfs -i size=1024 -f /dev/sdb1")
        run("mount /srv/node/sdb1")
        run("chown -R swift:swift /srv/node/sdb1")
