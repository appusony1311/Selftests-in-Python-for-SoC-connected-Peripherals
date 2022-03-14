*** Settings ***
Documentation          This is the Maschine Native OS Build eMMC Test.
...                    This is the minimun required for a build to be consided
...                    stable.
...                    ** This test suite must run in the TARGET board **
Library  ..${/}test_library${/}helper.py
Library  ..${/}test_library${/}emmc.py


*** Variables ***
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

