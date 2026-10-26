#!/bin/bash

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
echo "DIR IS '$DIR'"
cd $DIR

APP_INSTANCE=$(python3 -c "import instance; print(instance.APP_INSTANCE)")
PID_FILE="/var/run/obsreg_${APP_INSTANCE}.pid"

echo `pwd`
if [ ! -f gunicorn.pid ];then
        echo "No pid file, exiting"
else
        kill -15 `cat ${PID_FILE}`
        echo "Killed process from pid file"
        # Should wait and recheck and if still pid, then kill -9
fi

