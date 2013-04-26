from fabric.api import *

@task
def swift_all_start():
    with settings(parallel=True):
        run("swift-init all start")

@task
def swift_all_stop():
    with settings(parallel=True, warn_only=True):
        run("swift-init all stop")

@task
def swift_all_restart():
    run("swift-init all restart")

@task
@roles('swift_proxy')
def swift_proxy_start():
    run("swift-init proxy start")

@task
@roles('swift_proxy')
def swift_proxy_stop():
    run("swift-init proxy stop")

def swift_rest_start():
    run("swift-init rest start")

def swift_rest_stop():
    run("swift-init rest stop")

def swift_proxy_restart():
    run("swift-init proxy restart")

def swift_rest_restart():
    run("swift-init rest restart")

@roles('swift_proxy')
def copy_ring_files():
    for node in env.roledefs['swift_nodes_public']:
        run('scp /etc/swift/*.ring.gz root@{0}:/etc/swift'.format(node))

@roles('swift_proxy')
def _add_nodes_to_ring():
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

@task
def add_nodes_to_ring():
    _add_nodes_to_ring()
    ring_rebalance()
    copy_ring_files()

def delete_data():
    with settings(parallel=True):
        run("umount /srv/node/sdb1")
        run("mkfs.xfs -i size=1024 -f /dev/sdb1")
        run("mount /srv/node/sdb1")
        run("chown -R swift:swift /srv/node/sdb1")