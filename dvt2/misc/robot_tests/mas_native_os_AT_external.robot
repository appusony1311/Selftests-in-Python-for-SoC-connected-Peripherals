*** Settings ***
Documentation          This is the Maschine Native OS Build Acceptance Test.
...                    This is the minimun required for a build to be consided
...                    stable.
...                    ** This test suite must run in the TEST board **
Resource          shared_keywords.robot
Resource          shared_variables.robot
Suite Teardown    Teardown Remote OTG G Multi
Library           ..${/}test_library${/}helper.py
Library           ..${/}test_library${/}otg_ni.py


*** Variables ***


*** Test Cases ***
Should Ping Succeed
    ${rc} =     Is Ping Succeeded     ${IP}
    Should Be True    ${rc}

System Reboot And Verification
    ${pre_uptime_since} =    System Uptime    ${IP}    arg=s
    System Reboot Device    ${IP}
    Sleep    5s    #wait a little bit to in fact be rebooted
    Wait Until Device Is Pingable    ${IP}
    ${new_uptime_since} =    System Uptime    ${IP}    arg=s
    Should Not Be Equal As Strings    ${pre_uptime_since}    ${new_uptime_since}
    ${uptime_pretty} =    System Uptime    ${IP}    arg=p
    Should Be Equal As Strings    ${uptime_pretty}    up   #just up means up to 0m

System Shutdown HW Poweron And Verification
    ${pre_uptime_since} =    System Uptime    ${IP}    arg=s
    System Shutdown Device    ${IP}
    Wait Until Device Is Not Pingable    ${IP}
    Sleep    5s    #wait until the showdown process to finish
    Hw Poweron Device
    Wait Until Device Is Pingable    ${IP}
    ${new_uptime_since} =    System Uptime    ${IP}    arg=s
    Should Not Be Equal As Strings    ${pre_uptime_since}    ${new_uptime_since}
    ${uptime_pretty} =    System Uptime    ${IP}    arg=p
    Should Be Equal As Strings    ${uptime_pretty}    up   # `up` means up to 0m

The OTG Mass Storage Feature Should Be Working
    Setup OTG G Multi
    Run dd    ${/}dev${/}${LOC_OTG_PARTI_PATH}    ${LOC_OTG_BLOB_PATH}    ${REM_OTG_BLOB_SIZE}    1M
    Calc Remote Md5sum    ${IP}    ${REM_OTG_BLOB_PATH}    ${REM_OTG_BLOB_MD5_PATH}
    Calc Md5 Out File     ${LOC_OTG_BLOB_PATH}    ${LOC_OTG_BLOB_MD5_PATH}
    ${remote_md5} =     Get Remote Md5sum     ${IP}    ${REM_OTG_BLOB_MD5_PATH}
    ${local_md5} =      Get Md5sum     ${LOC_OTG_BLOB_MD5_PATH}
    Should Be Equal As Strings    ${remote_md5}    ${local_md5}


Test OTG Ether Feature Should Be Working
    ${ret} =     Is Ping Succeeded     ${REM_OTG_ETHER_IP}
    Should Be True    ${ret}
