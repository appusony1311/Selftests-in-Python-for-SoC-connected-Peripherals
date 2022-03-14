#!/bin/bash

: ${READPOINT=/dev/mmcblk1}

while [ true ]
do
    dd if=${READPOINT} of=/dev/null bs=512 count=2048000 iflag=nocache
done
