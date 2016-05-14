#!/usr/bin/env python
from app import app
from os import listdir
from app.models import PeeringSession
config = {
    'dir_interfaces': '/etc/network/interfaces.d',
          }
file_sessions = listdir(config['dir_interfaces'])
db_sessions=PeeringSession.query.filter_by(tunneltype_id=1)


