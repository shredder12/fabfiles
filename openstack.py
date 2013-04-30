from fabric.api import *

@task
def compute_restart():
    run("service nova-compute restart")