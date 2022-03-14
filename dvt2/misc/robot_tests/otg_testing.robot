*** Settings ***
Documentation          OTG Mass Storage Testing.
...                    The proper setup should be done before running (see otg_ni test library)
...                    ** This test suite must run in the TEST board **
Resource          shared_keywords.robot
Resource          shared_variables.robot
Suite Setup       Setup OTG G Multi
Suite Teardown    Teardown Remote OTG G Multi
Library           Collections
Library           ..${/}test_library${/}otg_ni.py
Library           ..${/}test_library${/}helper.py
Library           ..${/}test_library${/}network.py

*** Variables ***
${JSON_FILENAME}             json_result
@{ITERATION}                 1M   512K   1K   128


*** Test Cases ***
Test OTG Mass Storage
    : FOR   ${BS}    IN    @{ITERATION}
    \    Run dd    ${/}dev${/}${LOC_OTG_PARTI_PATH}    ${LOC_OTG_BLOB_PATH}    ${REM_OTG_BLOB_SIZE}    ${BS}
    \    Calc Remote Md5sum    ${IP}    ${REM_OTG_BLOB_PATH}    ${REM_OTG_BLOB_MD5_PATH}
    \    Calc Md5 Out File     ${LOC_OTG_BLOB_PATH}    ${LOC_OTG_BLOB_MD5_PATH}
    \    ${remote_md5} =     Get Remote Md5sum     ${IP}    ${REM_OTG_BLOB_MD5_PATH}
    \    ${local_md5} =      Get Md5sum     ${LOC_OTG_BLOB_MD5_PATH}
    \    Should Be Equal As Strings    ${remote_md5}    ${local_md5}


Test OTG Ether
    ${ret} =     Is Ping Succeeded     ${REM_OTG_ETHER_IP}
    Should Be True    ${ret}

    Start Remote Iperf3 Server    ${IP}
    ${ret} =     Is Remote Iperf3 Server Running    ${IP}
    Should Be True    ${ret}

    ${filepath} =     Start Iperf3 Client    ${IP}    ${JSON_FILENAME}     -J
    ${dict} =    Decode Iperf3 Json     ${filepath}
    ${sent_sum} =    Get Iperf3 Sent Summary    ${dict}
    ${mb} =     Get From Dictionary    ${sent_sum}    mb
    ${mb_per_second} =     Get From Dictionary    ${sent_sum}    mb_per_second
    ${MB_per_second} =     Evaluate      ${mb_per_second} / 8
    Should Be True      ${MB_per_second} >= 10 # bigger than 10 MB/s

    Kill Remote Iperf3 Server    ${IP}
