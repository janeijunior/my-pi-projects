#!/bin/bash

VIDEO_DEV="/dev/video0"
FRAME_RATE="5"
RESOLUTION="320x240"
PORT="5005"
YUV="true"

MJPG_STREAMER_DIR="$(dirname $0)"
MJPG_STREAMER_BIN="mjpg_streamer"
LOG_FILE="${MJPG_STREAMER_DIR}/mjpg-streamer.log"
RUNNING_CHECK_INTERVAL="30" # how often to check to make sure the server is running (in seconds)
HANGING_CHECK_INTERVAL="40" # how often to check to make sure the server is not hanging (in seconds)

function parseAdditionalArguments() {
    if [ "$2" != "" ]; then
        PORT=$2
    fi
    if [ "$3" != "" ]; then
        RESOLUTION=$3
    fi
    if [ "$4" != "" ]; then
        FRAME_RATE=$4
    fi

	echo $PORT $RESOLUTION $FRAME_RATE
}

function running() {
    if ps aux | grep ${MJPG_STREAMER_BIN} | grep ${VIDEO_DEV} >/dev/null 2>&1; then
        return 0

    else
        return 1

    fi
}

function start() {
    if running; then
        echo "already started"
        return 1
    fi

    export LD_LIBRARY_PATH="${MJPG_STREAMER_DIR}:."
    
    INPUT_OPTIONS="-r ${RESOLUTION} -d ${VIDEO_DEV} -f ${FRAME_RATE}"
    if [ "${YUV}" == "true" ]; then
        INPUT_OPTIONS+=" -y"
    fi
    
    OUTPUT_OPTIONS="-p ${PORT} -w www"
    
    ${MJPG_STREAMER_DIR}/${MJPG_STREAMER_BIN} -i "input_uvc.so ${INPUT_OPTIONS}" -o "output_http.so ${OUTPUT_OPTIONS}" >> ${LOG_FILE} 2>&1 &

    sleep 1

    if running; then
        if [ "$1" != "nocheck" ]; then
            check_running & > /dev/null 2>&1 # start the running checking task
            check_hanging & > /dev/null 2>&1 # start the hanging checking task
        fi

        echo "started"
        return 0

    else
        echo "failed to start"
        return 1

    fi
}

function stop() {
    if ! running; then
        echo "not running"
        return 1
    fi

    own_pid=$$

    if [ "$1" != "nocheck" ]; then
        # stop the script running check task
        ps aux | grep $0 | grep start | tr -s ' ' | cut -d ' ' -f 2 | grep -v ${own_pid} | xargs -r kill
        sleep 0.5
    fi

    # stop the server
    ps aux | grep ${MJPG_STREAMER_BIN} | grep ${VIDEO_DEV} | tr -s ' ' | cut -d ' ' -f 2 | grep -v ${own_pid} | xargs -r kill

    echo "stopped"
    return 0
}

function check_running() {
    echo "starting running check task" >> ${LOG_FILE}

    while true; do
        sleep ${RUNNING_CHECK_INTERVAL}

        if ! running; then
            echo "server stopped, starting" >> ${LOG_FILE}
            start nocheck
        fi
    done
}

function check_hanging() {
    echo "starting hanging check task" >> ${LOG_FILE}

    while true; do
        sleep ${HANGING_CHECK_INTERVAL}

        # treat the "error grabbing frames" case
        if tail -n2 ${LOG_FILE} | grep -i "error grabbing frames" > /dev/null; then
            echo "server is hanging, killing" >> ${LOG_FILE}
            stop nocheck
        fi
    done
}

function help() {
    echo "Usage: $0 [start|stop|restart|status] [port number] [resolution] [framerate]"
    return 0
}

if [ "$1" == "start" ]; then
    parseAdditionalArguments "$@"
    start && exit 0 || exit -1

elif [ "$1" == "stop" ]; then
    stop && exit 0 || exit -1

elif [ "$1" == "restart" ]; then
    stop && sleep 1
    start && exit 0 || exit -1

elif [ "$1" == "status" ]; then
    if running; then
        echo "running"
        exit 0

    else
        echo "stopped"
        exit 1

    fi

else
    help

fi
