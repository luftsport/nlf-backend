#!/bin/bash

WORKING_DIR="${PWD}/"



SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
echo "DIR IS '$DIR'"

cd $DIR

GUNICORN="${DIR}/bin/gunicorn"


if [[ INVENV == 0 ]]
then
        source bin/activate
fi

INVENV=$(python -c 'import sys; print ("1" if hasattr(sys, "real_prefix") else "0")')

APP_INSTANCE=$(python3 -c "import instance; print(instance.APP_INSTANCE)")
PID_FILE="/var/local/run/obsreg_${APP_INSTANCE}/obsreg_${APP_INSTANCE}.pid"
umask 0022

# PROD
if [[ APP_INSTANCE == "prod" ]]
then
  echo "Starting PROD instance"
  $GUNICORN -w 5 -b localhost:8081 run:app --log-level=debug --log-file=unicorn.log --pid "$PID_FILE" --capture-output --enable-stdio-inheritance --daemon
fi

# DEV
if [[ APP_INSTANCE == "dev" ]]
then
  echo "Starting DEV instance"
  $GUNICORN  -w 4 -b localhost:8082 run:app --log-level=debug --log-file=unicorn.log --pid gunicorn.pid --capture-output --enable-stdio-inheritance --daemon
fi

# DEV
if [[ APP_INSTANCE == "local" ]]
then
  echo "Starting LOCAL instance"
  echo "Sure you do not want to start using the development server as python run.py?"
  $GUNICORN  -w 1 -b localhost:8082 run:app --log-level=debug --log-file=unicorn.log --pid gunicorn.pid --capture-output --enable-stdio-inheritance --daemon
fi

if [[ INVENV == 0 ]]
then
        deactivate
fi

# Check if notification service is running
SERVICE="obsreg_notifications.service"

if systemctl is-active --quiet "$SERVICE"; then
    echo "$SERVICE is running."
else
    echo "$SERVICE is stopped or failed."
fi

cd
