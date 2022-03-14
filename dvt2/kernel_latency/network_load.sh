#!/bin/bash

download_file=https://cdn.kernel.org/pub/linux/kernel/v4.x/linux-4.14.44.tar.xz
wget_output=output
file_output=/tmp/

while [ true ]
do
    wget -o ${wget_output} -P ${file_output} ${download_file}
    rm /tmp/linux-4.14.44.tar.xz
    rm ${wget_output}
done
