#!/usr/bin/env bash

#variables
: ${INTERVAL=30}

filename="current_cpu_clock.txt"

printf "CPU0,CPU1,CPU2,CPU3\n" >> ${filename}
while [ true ]
do
    cpu0=$(awk '{ print }' /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq)
    cpu1=$(awk '{ print }' /sys/devices/system/cpu/cpu1/cpufreq/scaling_cur_freq)
    cpu2=$(awk '{ print }' /sys/devices/system/cpu/cpu2/cpufreq/scaling_cur_freq)
    cpu3=$(awk '{ print }' /sys/devices/system/cpu/cpu3/cpufreq/scaling_cur_freq)
    printf "$cpu0,$cpu1,$cpu2,$cpu3\n" >> ${filename}
    sleep ${INTERVAL}
done