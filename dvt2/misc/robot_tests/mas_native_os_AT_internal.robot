*** Settings ***
Documentation          This is the Maschine Native OS Build Acceptance Test.
...                    This is the minimun required for a build to be consided
...                    stable.
...                    ** This test suite must run in the TARGET board **
Library  ..${/}test_library${/}helper.py
Library  ..${/}test_library${/}cpufreq.py
Library  ..${/}test_library${/}cpuidle.py
Library  ..${/}test_library${/}dbus_systemd.py
Library  ..${/}test_library${/}emmc.py


*** Variables ***
${MAS_SERV_NAME}       maschine

${EMMC_STORAGE_SIZE}                 29184
${EMMC_BOOT_SIZE}                       40
${EMMC_RUN_MEDIA_MMCBLK1P2_SIZE}      1024
${EMMC_ROOT_SIZE}                    10200
${EMMC_SWAP_SIZE}                      512
${EMMC_USER_DATA_SIZE}                 512
${EMMC_FACTORY_LIB_SIZE}             16844

${EMMC_WRITE_SPEED}                     47
${EMMC_READ_SPEED}                     270

${EMMC_BOOT_MOUNTPOINT}                        /boot
${EMMC_RUN_MEDIA_MMCBLK1P2_MOUNTPOINT}         /run/media/mmcblk1p2
${EMMC_ROOT_MOUNTPOINT}                        /
${EMMC_SWAP_MOUNTPOINT}                        [SWAP]
${EMMC_USER_DATA_MOUNTPOINT}                   /user-data
${EMMC_FACTORY_LIB_MOUNTPOINT}                 /factory-lib


*** Test Cases ***
Should Physical Core Be Equal
    ${return} =     Get Physical Cores
    Should Be Equal As Integers    ${return}    ${4}

Should Maschine MK3 Controller Be Detectec by OS
    ${return} =     Is Maschine Usb Detected
    Should Be True    ${return} == True

Should Maschine MK3 Controller Be Detected By Alsa
    ${return} =     Is Maschine Alsa Detected
    Should Be True    ${return} == True

Should The CPU Model Be Equal
    ${return} =     Get Cpu Model
    Should Be Equal    ${return}    ${92}

Should The CPU Model Name Be Equal
    ${return} =     Get Cpu Model Name
    Should Be Equal    ${return}    Intel(R) Atom(TM) Processor E3940 @ 1.60GHz

Should The CPU Temp Not More than 60 Degrees
    ${return} =     Get Cpu Temp
    Should Be True    ${return} < ${60}

Should The Kernel Release Be Equal
    ${return} =     Get Kernel Release
    Should Be Equal    ${return}    4.14.71-rt44

Should The Arch HW Be Equal
    ${return} =     Get CPU Arch
    Should Be Equal    ${return}    x86_64

Should The CPU Max Freq Be Equal
    ${CORES} =            Get Physical Cores
    : FOR   ${INDEX}    IN RANGE    0    ${CORES}
    \   ${cpu_freq} =         Get Cpufreq Max Freq     core=${INDEX}
    \   Should Be Equal As Integers     ${cpu_freq}    ${1800}

Should The CPU Scaling Max Freq Be Equal
    ${CORES} =            Get Physical Cores
    : FOR   ${INDEX}    IN RANGE    0    ${CORES}
    \   ${cpu_freq} =         Get Scaling Max Freq     core=${INDEX}
    \   Should Be Equal As Integers     ${cpu_freq}    ${1800}

Should The CPU Min Freq Be Equal
    ${CORES} =            Get Physical Cores
    : FOR   ${INDEX}    IN RANGE    0    ${CORES}
    \   ${cpu_freq} =         Get Cpufreq Min Freq     core=${INDEX}
    \   Should Be Equal As Integers     ${cpu_freq}    ${800}

Should The CPU Scaling Min Freq Be Equal
    ${CORES} =            Get Physical Cores
    : FOR   ${INDEX}    IN RANGE    0    ${CORES}
    \   ${cpu_freq} =         Get Scaling Min Freq     core=${INDEX}
    \   Should Be Equal As Integers     ${cpu_freq}    ${800}

Should The CPU Max and CPU Scaling Max Freq Equal
    ${CORES} =            Get Physical Cores
    : FOR   ${INDEX}    IN RANGE    0    ${CORES}
    \   ${scaling_freq} =     Get Scaling Max Freq     core=${INDEX}
    \   ${cpu_freq} =         Get Cpufreq Max Freq     core=${INDEX}
    \   Should Be Equal As Integers     ${cpu_freq}    ${scaling_freq}

Should The CPU Min and CPU Scaling Min Freq Equal
    ${CORES} =            Get Physical Cores
    : FOR   ${INDEX}    IN RANGE    0    ${CORES}
    \   ${scaling_freq} =     Get Scaling Min Freq     core=${INDEX}
    \   ${cpu_freq} =         Get Cpufreq Min Freq     core=${INDEX}
    \   Should Be Equal As Integers     ${cpu_freq}    ${scaling_freq}

Should CPU Scaling Available Governors Be Equal
    ${CORES} =            Get Physical Cores
    : FOR   ${INDEX}    IN RANGE    0    ${CORES}
    \    ${governors} =    Get Scaling Available Governors    core=${INDEX}
    \    ${len} =    Get Length    ${governors}
    \    Should Be Equal    ${len}    ${2}
    \    Should Be Equal    @{governors}[${0}]    performance
    \    Should Be Equal    @{governors}[${1}]    powersave

Should CPU Scaling Governor Be Equal
    ${CORES} =            Get Physical Cores
    : FOR   ${INDEX}    IN RANGE    0    ${CORES}
    \    ${governor} =     Get Scaling Governor    core=${INDEX}
    \    Should Be Equal    ${governor}    performance

Should CPU Scaling Driver Be Equal
    ${CORES} =            Get Physical Cores
    : FOR   ${INDEX}    IN RANGE    0    ${CORES}
    \    ${driver} =     Get Scaling Driver    core=${INDEX}
    \    Should Be Equal    ${driver}    intel_pstate

Should CPU Idle Driver Be Equal
    ${CORES} =            Get Physical Cores
    : FOR   ${INDEX}    IN RANGE    0    ${CORES}
    \    ${driver} =     Get Cpuidle Cur Driver
    \    Should Be Equal    ${driver}    none

Should CPU Idle Governor Be Equal
    ${CORES} =            Get Physical Cores
    : FOR   ${INDEX}    IN RANGE    0    ${CORES}
    \    ${driver} =     Get Cpuidle Cur Governor
    \    Should Be Equal    ${driver}    menu

Should Emmc Device Size Be Equal
    ${SIZE} =     Get Emmc Size
    Should Be Equal As Integers    ${SIZE}     ${EMMC_STORAGE_SIZE} 

Should Emmc Boot Partition Size Be Equal
    ${SIZE} =     Get Size Of Mounted Partition    mmcblk1p1
    Should Be Equal As Integers    ${SIZE}     ${EMMC_BOOT_SIZE}

Should Emmc /run/media/mmcblk1p2 Partition Size Be Equal
    ${SIZE} =     Get Size Of Mounted Partition    mmcblk1p2
    Should Be Equal As Integers    ${SIZE}     ${EMMC_RUN_MEDIA_MMCBLK1P2_SIZE}

Should Emmc Root Partition Size Be Equal
    ${SIZE} =     Get Size Of Mounted Partition    mmcblk1p3
    Should Be Equal As Integers    ${SIZE}     ${EMMC_ROOT_SIZE} 

Should Emmc Swap Partition Size Be Equal
    ${SIZE} =     Get Size Of Mounted Partition    mmcblk1p4
    Should Be Equal As Integers    ${SIZE}     ${EMMC_SWAP_SIZE} 

Should Emmc User data Partition Size Be Equal
    ${SIZE} =     Get Size Of Mounted Partition    mmcblk1p5
    Should Be Equal As Integers    ${SIZE}     ${EMMC_USER_DATA_SIZE} 

Should Emmc Factory Lib Partition Size Be Equal
    ${SIZE} =     Get Size Of Mounted Partition    mmcblk1p6
    Should Be Equal As Integers    ${SIZE}     ${EMMC_FACTORY_LIB_SIZE} 

Log Emmc Serial Number
    ${SN} =    Get Emmc Serial Num

Should Emmc Mount Point Exists   
    ${RET} =     Is Mount Point Exists    ${EMMC_BOOT_MOUNTPOINT}  # boot partition
    Should Be True    ${RET}

    ${RET} =     Is Mount Point Exists    ${EMMC_RUN_MEDIA_MMCBLK1P2_MOUNTPOINT}  # mmcblk1p2 partition
    Should Be True    ${RET}

    ${RET} =     Is Mount Point Exists    ${EMMC_ROOT_MOUNTPOINT}  # root partition
    Should Be True    ${RET}

    ${RET} =     Is Swap Present          ${EMMC_SWAP_MOUNTPOINT}  # swap parition
    Should Be True    ${RET}

    ${RET} =     Is Mount Point Exists    ${EMMC_USER_DATA_MOUNTPOINT}  # user-data partition
    Should Be True    ${RET}

    ${RET} =     Is Mount Point Exists    ${EMMC_FACTORY_LIB_MOUNTPOINT}  # factory-lib partition
    Should Be True    ${RET}

Should Emmc Write Speed Not Exceed The Specs
     ${speed}     ${unit} =     Write perf    ${/}dev${/}urandom   emmc_speedtest    10M    1M
     Should Be True      ${speed} <= ${EMMC_WRITE_SPEED}  # to avoid wrong measuraments.

Should Emmc Read Speed Not Exceed The Specs
     ${speed}     ${unit} =     Read perf    emmc_speedtest  ${/}dev${/}null   10M    1M
     Should Be True      ${speed} <= ${EMMC_READ_SPEED}  # to avoid wrong measuraments.

# Should Systemd Maschine Service Be Loaded
#     ${return} =    Get Unit Load State     ${MAS_SERV_NAME}
#     Should Be Equal    ${return}    loaded

# Should Systemd Maschine Service Be Active
#     ${return} =    Get Unit Active State     ${MAS_SERV_NAME}
#     Should Be Equal    ${return}    active

# Should Systemd Maschine Service Be Running
#     ${return} =    Get Unit Substate     ${MAS_SERV_NAME}
#     Should Be Equal    ${return}    running

# Should Cpuidle States Be Enable
#     ${STATES} =    Get Cpuidle State Levels
#     ${CORES} =     Get Physical Cores
