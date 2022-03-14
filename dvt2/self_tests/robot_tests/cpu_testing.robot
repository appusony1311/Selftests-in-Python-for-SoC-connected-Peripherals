*** Settings ***
Documentation          This is the Maschine Native OS Build CPU Test.
...                    This is the minimun required for a build to be consided
...                    stable.
...                    ** This test suite must run in the TARGET board **
Library  ..${/}test_library${/}helper.py
Library  ..${/}test_library${/}cpufreq.py

*** Variables ***
${NUMBER_OF_CORES}                       4
${CPU_MODEL}                            92
${CPU_MODEL_NAME}                     Intel(R) Atom(TM) Processor E3940 @ 1.60GHz
${CPU_ARCH}                           x86_64
${CPU_MAX_FREQ}                       1800
${CPU_MIN_FREQ}                        800
${CPU_CUR_FREQ}                       1792

*** Test Cases ***
Should Physical Core Be Equal
    ${return} =     Get Physical Cores
    Should Be Equal As Integers    ${return}    ${NUMBER_OF_CORES}

Should The CPU Model Be Equal
    ${return} =     Get Cpu Model
    Should Be Equal As Strings    ${return}    ${CPU_MODEL}

Should The CPU Model Name Be Equal
    ${return} =     Get Cpu Model Name
    Should Be Equal As Strings    ${return}    ${CPU_MODEL_NAME}

Should The Arch HW Be Equal
    ${return} =     Get CPU Arch
    Should Be Equal    ${return}    ${CPU_ARCH}

Should The CPU Max Freq Be Equal (in MHz)
    ${CORES} =            Get Physical Cores
    : FOR   ${INDEX}    IN RANGE    0    ${CORES}
    \   ${cpu_freq} =         Get Cpufreq Max Freq     core=${INDEX}
    \   Should Be Equal As Integers     ${cpu_freq}    ${CPU_MAX_FREQ}

Should The CPU Min Freq Be Equal (in MHz)
    ${CORES} =            Get Physical Cores
    : FOR   ${INDEX}    IN RANGE    0    ${CORES}
    \   ${cpu_freq} =         Get Cpufreq Min Freq     core=${INDEX}
    \   Should Be Equal As Integers     ${cpu_freq}    ${CPU_MIN_FREQ}

Get The Current CPU Freq (in MHz)
    ${CORES} =            Get Physical Cores
    : FOR   ${INDEX}    IN RANGE    0    ${CORES}
    \   ${cpu_freq} =         Get Scaling Cur Freq     core=${INDEX}
    \   Should Be True      ${cpu_freq} >= ${CPU_CUR_FREQ}



