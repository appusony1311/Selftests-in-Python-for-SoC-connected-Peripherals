*** Keywords ***
Setup OTG G Multi
    # create a blob file in the remote target
    Run Remote Dd    ${IP}    /dev/urandom    ${REM_OTG_BLOB_PATH}     ${REM_OTG_BLOB_SIZE}      1M
    Setup Remote Congatec Qeva2 G Multi     ${IP}    ${REM_OTG_BLOB_PATH}
    Sleep      2s
    ${ret} =    Is Remote Otg G Multi Enabled     ${IP}
    Sleep      2s
    Enable Remote OTG G Multi IP     ${IP}    ${REM_OTG_ETHER_IP}
    Sleep      2s
    ${remote_otg_ip} =     Get Remote OTG G Multi IP     ${IP}
    Should Be Equal As Strings    ${remote_otg_ip}     ${REM_OTG_ETHER_IP}
    ${ret} =    Is Fsg Present
    Should Be True    ${ret}
    Set Otg Ether Ip      ${LOC_OTG_ETHER_IP}
    ${ret} =    Get Otg Ether Ip
    Should Be Equal As Strings    ${LOC_OTG_ETHER_IP}     ${ret}


Teardown Remote OTG G Multi
    Disable Remote OTG G Multi     ${IP}
    ${ret} =    Is Remote Otg G Multi Enabled     ${IP}
    Should Not Be True    ${ret}
