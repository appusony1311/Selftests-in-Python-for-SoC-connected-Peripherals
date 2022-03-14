#!/usr/bin/env bash

# global variables
: ${CPU=4}
: ${IO=4}
: ${VM=4}
: ${HDD=1}
: ${HDD-BYTES=256M}
: ${LONG=720} # minutes

# trap ctrl-c and call ctrl_c()
trap ctrl_c INT

function ctrl_c() {
    echo "** Trapped CTRL-C"
    tear_down
    exit 1
}

function tear_down() {
    echo "TEAR DOWN"
    sync
    killall stress 2> /dev/null
    killall hackbench 2> /dev/null
    killall sar 2> /dev/null

    # getting max latency from cyclictest output file
    echo "GET MAX LATENCY"
    python ../get_max_latency.py

    # getting max temperature and minimum frequency
    echo "POS PROCESS"
    python ../pos_process.py

    # compressing the results into a single file
    cd ..
    cdate="$(date +%Y_%m_%d_%H_%M_%S)"
    tar cvfz ${cdate}_${BENCHMARK_NAME}.tar.gz ${FOLDER_RESULT}/

    killall sh
}

# variables
FOLDER_RESULT=benchmark_test
BENCHMARK_NAME=worst_case_scenario

PRIO=90

# sar variables
SAR_FREQ=30

# setup
echo -e "SETUP... "
if [ -d ${FOLDER_RESULT} ]
then
    rm -r ${FOLDER_RESULT}
fi

mkdir -p ${FOLDER_RESULT}
cd ${FOLDER_RESULT}
echo "OK"
##############################################################################


# system load
echo -e "SYSTEM LOAD... "
stress --cpu ${CPU} --io ${IO} --vm ${VM} --hdd ${HDD} --hdd-bytes ${HDD-BYTES} > /dev/null &
hackbench -l 100000000000000 1> /dev/null &

sh ../sdcard_load.sh &
sh ../network_load.sh &
echo "OK"
##############################################################################


# system monitoring
echo -e "SYSTEM MONITORING... "
sar -u ${SAR_FREQ} -P ALL > sar_cpu_mon.txt &
sar -b ${SAR_FREQ} > sar_io_mon.txt &
sar -r ${SAR_FREQ} > sar_mem_mon.txt &
sar -w ${SAR_FREQ} > sar_kernel_mon.txt &
sar -W ${SAR_FREQ} > sar_swapping_mon.txt &
sar -n DEV ${SAR_FREQ} > sar_network_mon.txt &

sh ../temp_mon.sh &
sh ../current_cpu_clock.sh &
echo "OK"
##############################################################################

# benchmarking
echo "BENCHMARKING"
if [ "$1" = "-b" ]; then
    echo Running cyclictest with ftrace with tracebreak = $2
    sysctl kernel.ftrace_enabled=1
    trace-cmd start -b 20000 -p function -l '*spin_*' -l '*mutex*' -e all
    cyclictest -D ${LONG}m -m -Sp${PRIO} -i200 -h600 -q -b $2 > cyclictest_output.txt
    trace-cmd extract
else
    cyclictest -D ${LONG}m  -m -Sp${PRIO} -i200 -h600 -q > cyclictest_output.txt
fi

# tear down
tear_down
