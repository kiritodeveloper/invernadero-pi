#!/bin/bash
### BEGIN INIT INFO
# Provides:          apache2
# Required-Start:    $local_fs $remote_fs $network $syslog $named
# Required-Stop:     $local_fs $remote_fs $network $syslog $named
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# X-Interactive:     true
# Short-Description: Python Flask start
# Description:       Start the web server flask
#  This script will start the flask web server.
### END INIT INFO

cd ~/webfinvernadero/
source ~/webfinvernadero/.initflask
source ~/webfinvernadero/venv/bin/activate
flask run --host=0.0.0.0 &
sleep 10
cd /tmp/
wget  http://localhost:5000/auth/login
