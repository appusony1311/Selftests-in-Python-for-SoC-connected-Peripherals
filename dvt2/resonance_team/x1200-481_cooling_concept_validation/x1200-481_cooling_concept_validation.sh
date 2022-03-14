#!/bin/bash

# This code is meant to be run in the Intel Atom E3940.
# It is arch dependent.

CPU_NUM=4
RESULT_FOLDER=~
PERIOD=1
TEMP_FILE=/sys/class/hwmon/hwmon1/temp1_input

mkdir -p $RESULT_FOLDER

# stress the cpu (also forking)
stress --cpu ${CPU_NUM} &

#current date
cdate="$(date +%Y_%m_%d_%H_%M_%S)"

while [ true ]
do
    cat ${TEMP_FILE} >> ${RESULT_FOLDER}/temp_${cdate}
    # forcing flushing caching data to the disk to avoid losing data in case of shutdown.
    sync
    sleep ${PERIOD}
done