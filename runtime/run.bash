#!/bin/bash

bash tools/rm_ipcs.bash

ASSET_DEF="data/asset_def.txt"

HAKO_CONDUCTOR_PID=
HAKO_ASSET_PROG_PID=
IS_OCCURED_SIGEVENT="FALSE"
function signal_handler()
{
    IS_OCCURED_SIGEVENT="TRUE"
}
function kill_process()
{
    echo "trapped"
    if [ -z "$HAKO_CONDUCTOR_PID" ]
    then
        exit 0
    fi
    
    # HAKO_ASSET_PROG_PID に保存されている各PIDをkill
    for pid in $HAKO_ASSET_PROG_PID; do
        echo "KILLING: ASSET PROG $pid"
        kill -s TERM $pid || echo "Failed to kill ASSET PROG $pid"
    done
    
    echo "KILLING: hakoniwa-conductor $HAKO_CONDUCTOR_PID"
    kill -9 "$HAKO_CONDUCTOR_PID" || echo "Failed to kill hakoniwa-conductor"

    while [ 1 ]
    do
        NUM=$(ps aux | grep hakoniwa-conductor | grep -v grep | wc -l)
        if [ $NUM -eq 0 ]
        then
            break
        fi
        sleep 1
    done

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

trap signal_handler SIGINT SIGTERM

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

function activate()
{
    HAKO_ASSET_PROG_PID=
    for entry in `cat ${ASSET_DEF}`
    do
        RUNTYPE=`echo ${entry} | awk -F: '{print $1}'`
        PROG_NAME=`echo ${entry}  | awk -F: '{print $2}'`
        ARG1=`echo ${entry}  | awk -F: '{print $3}'`
        echo "INFO: ACTIVATING :${RUNTIPE} ${PROG_NAME} ${ARG1}"
        if [ ${RUNTYPE} = "python" ]
        then
            python ${PROG_NAME} ${ARG1} &
            HAKO_ASSET_PROG_PID="$! ${HAKO_ASSET_PROG_PID}"
        else
            ${PROG_NAME} ${ARG1} &
            HAKO_ASSET_PROG_PID="$! ${HAKO_ASSET_PROG_PID}"
        fi
        sleep 1
    done
    echo "PIDS= ${HAKO_ASSET_PROG_PID}"
}

activate

echo "START"
while true; do
    echo "Press ENTER to stop..."
    read input
    if [ -z "$input" ]; then
        kill_process
        break
    fi
done
