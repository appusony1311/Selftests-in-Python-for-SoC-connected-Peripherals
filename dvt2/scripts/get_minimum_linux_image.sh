#!/bin/bash

#  OVERVIEW
#  If `no wic image` is found, it downloads it (also md5 file). 
#     It calculates its md5 checksum and compared to the provided md5 file.
#    
#  If a `wic file` is found, it downloads the current md5 file from server, 
#    it compares to the calculated md5 file.
#      If equal: --> Do not anything else
#      If diff: --> Download the current `wic file`, calculate its
#                   checksum, compared to the provided md5 file.
#
# Script to be run on the Jenkins server


# env variables
: ${MINIMAL_IMAGE=maschine-image-minimal-congatec-tca5-64.wic}
: ${BASE_PATH=/maschine/}
: ${IP=10.1.9.20}

# helper functions
function clean_up_files() {
    echo "Removing the minimal image & calculated md5 from workspace"
    rm ${MINIMAL_IMAGE} ${MINIMAL_IMAGE_MD5} ${CALCULATED_MD5}
}

function download_minimal_files() {
    echo "Downloading minimal wic & md5 files"
    wget -q http://${IP}${BASE_PATH}${MINIMAL_IMAGE}
    wget -q http://${IP}${BASE_PATH}${MINIMAL_IMAGE_MD5}
}

function calculate_md5_and_save_to_file() {
    echo "Calculating "${MINIMAL_IMAGE}" md5 checksum"

    calc_md5="$(md5sum ${MINIMAL_IMAGE})"
    calc_md5="$(echo ${calc_md5} | awk '{print $1}')"

    echo "Copying it to the "${CALCULATED_MD5}" file"
    echo ${calc_md5} > ${CALCULATED_MD5}
}


# internal variables
MINIMAL_IMAGE_MD5=${MINIMAL_IMAGE}.md5
CALCULATED_MD5=calculated_md5.md5


# main script
if [ -f ${MINIMAL_IMAGE} ]
then
    echo "File "${MINIMAL_IMAGE}" found!"
    if [ -f ${MINIMAL_IMAGE_MD5} ]
    then
        echo "Removing old version of "${MINIMAL_IMAGE_MD5}
        rm ${MINIMAL_IMAGE_MD5}
    fi

    echo "Downloading from server the new md5 file "${MINIMAL_IMAGE_MD5}
    wget -q http://${IP}${BASE_PATH}${MINIMAL_IMAGE_MD5}
    diff ${MINIMAL_IMAGE_MD5} ${CALCULATED_MD5} > /dev/null
    ret="$(echo $?)"
    if [ ${ret} -ne 0 ]
    then
        echo "The "${MINIMAL_IMAGE_MD5}" and "${CALCULATED_MD5}" do not match"
        clean_up_files
        download_minimal_files
        calculate_md5_and_save_to_file

        diff ${MINIMAL_IMAGE_MD5} ${CALCULATED_MD5} > /dev/null
        ret="$(echo $?)"
        if [ ${ret} -ne 0 ]
        then
            echo "ERROR: The calculated md5 and provided md5 do not match"
            echo "ERROR: Start it all over"
        else
            echo "DONE: All OK, The MD5 files matched"
        fi
    else
        echo "DONE: All OK, The MD5 files matched"
    fi
else
    echo "File "${MINIMAL_IMAGE}" not found!"
    download_minimal_files

    calculate_md5_and_save_to_file

    diff ${MINIMAL_IMAGE_MD5} ${CALCULATED_MD5} > /dev/null
    ret="$(echo $?)"
    if [ ${ret} -ne 0 ]
    then
        echo "ERROR: The calculated md5 and provided md5 do not match"
        echo "ERROR: Start it over"
    else
        echo "DONE: All OK"
    fi
fi