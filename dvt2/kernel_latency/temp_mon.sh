#!/usr/bin/env bash

#setup
: ${INTERVAL=30}

filename=thermal_mon.txt

printf "physical_id_0,CPU0,CPU1,CPU2,CPU3\n" >> ${filename}
while [ true ]
do
    phy=$(awk '{ print }' /sys/class/hwmon/hwmon1/temp1_input)
    cpu0=$(awk '{ print }' /sys/class/hwmon/hwmon1/temp2_input)
    cpu1=$(awk '{ print }' /sys/class/hwmon/hwmon1/temp3_input)
    cpu2=$(awk '{ print }' /sys/class/hwmon/hwmon1/temp4_input)
    cpu3=$(awk '{ print }' /sys/class/hwmon/hwmon1/temp5_input)
    printf "$phy,$cpu0,$cpu1,$cpu2,$cpu3\n" >> ${filename}
    sleep ${INTERVAL}
done