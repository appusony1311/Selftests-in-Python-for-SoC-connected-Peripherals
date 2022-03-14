#!/bin/bash -x

# Script for waiting a board to be connected to the internet.
# This code is suppose to be run on Jenkins.

# env variables
: ${INTERVAL=5}
: ${ATTEMPTS=8}
: ${IP=10.1.9.22}

# local variables
counter=0

while [ true ]
do
    ping -w 3 ${IP}
    ret=$(echo $?)

    if [ ${ret} -eq 0 ]
    then 
        exit 0 
    fi

    if [ ${counter} -gt ${ATTEMPTS} ]
    then
        echo "Time out"
        exit 2 # exit == 2 for unstable build on Jenkins
    fi

    let counter++
    sleep ${INTERVAL}
done
