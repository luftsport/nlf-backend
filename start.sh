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

INVENV=$(python -c 'import sys; print ("1" if hasattr(sys, "real_prefix") else "0")')


if [[ INVENV == 0 ]]
then
        source bin/activate
fi
# PROD
$GUNICORN -w 5 -b localhost:8081 run:app --log-level=debug --log-file=unicorn.log --pid gunicorn.pid --capture-output --enable-stdio-inheritance --daemon
# DEV
# $GUNICORN  -w 4 -b localhost:8082 run:app --log-level=debug --log-file=unicorn.log --pid gunicorn.pid --capture-output --enable-stdio-inheritance --daemon
if [[ INVENV == 0 ]]
then
        deactivate
fi

cd
