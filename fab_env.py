from fabric.api import *
from roles import roles_dict

env.user = "root"
env.roledefs = roles_dict