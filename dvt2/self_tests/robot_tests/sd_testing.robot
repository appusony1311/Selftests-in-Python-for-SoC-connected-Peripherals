*** Settings ***
Documentation          This is the Maschine Native OS Build SD Test.
...                    This is the minimun required for a build to be consided
...                    stable.
...                    ** This test suite must run in the TARGET board **
Library  ..${/}test_library${/}helper.py
Library  ..${/}test_library${/}sd.py


*** Variables ***
${SD_FSTYPE}                           vfat
${SD_MOUNTPOINT}                       /run/media/mmcblk0p1
${SD_DEVICE_FILE}                      /dev/mmcblk0p1
${SPEED_TEST}                          /run/media/mmcblk0p1/sd_speedtest

*** Test Cases ***
Log SD Storage Size in MB
    ${SIZE} =     Get Sd Size

Log SD size Partition
    ${SIZE} =     Get Size Of Mounted Partition    mmcblk0p1

Log SD Serial Number
    ${SN} =    Get SD Serial Num

Should SD Mount Point Exists   
    ${RET} =     Is Mount Point Exists    ${SD_MOUNTPOINT}
    Should Be True    ${RET}

Should SD Filesystem type be vfat
    ${RET} =     Get Fstype Of Mounted Partition   ${SD_DEVICE_FILE}
    Should Be Equal    ${RET}    ${SD_FSTYPE}

Log SD Write Speed in MB/s
     ${speed}     ${unit} =     Write perf    ${/}dev${/}urandom   ${SPEED_TEST}    10M    1M

Log SD Read Speed in MB/s
     ${speed}     ${unit} =     Read perf    ${SPEED_TEST}  ${/}dev${/}null   10M    1M

