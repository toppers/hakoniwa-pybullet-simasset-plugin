#!/bin/bash


ASSET_ACT_MODE="PYTHON"
if [ $# -eq 1 ]
then
    echo "INFO: ROS MODE"
    ASSET_ACT_MODE="ROS"
else
    echo "INFO: PYTHON MODE"
fi
ASSET_DEF="data/asset_def.txt"

HAKO_CONDUCTOR_PID=
HAKO_ASSET_PROG_PID=
function signal_handler()
{
    echo "trapped"
    if [ -z ${HAKO_CONDUCTOR_PID} ]
    then
        exit 0
    fi
    if [ -z ${HAKO_CONDUCTOR_PID} ]
    then
        :
    else
        if [ ! -z ${HAKO_ASSET_PROG_PID} ]
        then
            echo "KILLING: ASSET PROG ${HAKO_ASSET_PROG_PID}"
            kill -s TERM ${HAKO_ASSET_PROG_PID}
        fi
    fi
    echo "KILLING: hakoniwa-conductor ${HAKO_CONDUCTOR_PID}"
    kill -s TERM ${HAKO_CONDUCTOR_PID}

    exit 0
}

OLD_PID=`ps aux | grep hakoniwa-conductor | grep -v grep | awk '{print $2}'`
if [ -z $OLD_PID ] 
then
    :
else
    echo "KILLING old pid: ${OLD_PID}"
    kill -s TERM $OLD_PID
fi

trap signal_handler SIGINT

export PATH="/usr/local/bin/hakoniwa:${PATH}"
export LD_LIBRARY_PATH="/usr/local/lib/hakoniwa:${LD_LIBRARY_PATH}"
export DYLD_LIBRARY_PATH="/usr/local/lib/hakoniwa:${DYLD_LIBRARY_PATH}"

DELTA_MSEC=20
MAX_DELAY_MSEC=100
CORE_IPADDR=127.0.0.1
GRPC_PORT=50051
echo "INFO: ACTIVATING HAKONIWA-CONDUCTOR"
hakoniwa-conductor ${DELTA_MSEC} ${MAX_DELAY_MSEC} ${CORE_IPADDR}:${GRPC_PORT}   &  
HAKO_CONDUCTOR_PID=$!

sleep 1

function activate_python()
{
    HAKO_ASSET_PROG_PID=
    for entry in `cat ${ASSET_DEF}`
    do
        PYTHON_PROG=`echo ${entry}  | awk -F: '{print $1}'`
        ARG1=`echo ${entry}  | awk -F: '{print $2}'`
        echo "INFO: ACTIVATING :${PYTHON_PROG} ${ARG1}"
        python ${PYTHON_PROG} ${ARG1} &
        HAKO_ASSET_PROG_PID="$! ${HAKO_ASSET_PROG_PID}"
        sleep 1
    done
}

if [ $ASSET_ACT_MODE = "PYTHON" ]
then
    activate_python
else
    :
fi

echo "START"
while [ 1 ]
do
    sleep 100
done
