*** Settings ***
Documentation          This is the Maschine Native OS Build Wi-Fi Test.
...                    This is the minimun required for a build to be consided
...                    stable.
...                    ** This test suite must run in the TARGET board **
Library  ..${/}test_library${/}helper.py
Library  ..${/}test_library${/}wifi.py


*** Variables ***
${SSID}                           NIFunkloch
${PW}                             0160712657364906
${SIGNAL_LEVEL_THRESHOLD}         -90

*** Test Cases ***
List Wi-Fi Access points
    Wifi List Accesspoints

Connect Wi-Fi to Access point
    ${RET} =     Wifi Disconnect Then Connect      ${SSID}      ${PW}
    Log    WIFI SSID: ${SSID}
    Log    WIFI PW: ${PW}
    Should Be True    ${RET}

Check for Wi-Fi Connectivity
    ${RET} =    Wifi Connect Verify
    Should Be True    ${RET}    

Get Gateway IP and Check Whether Wi-Fi is Pingable
    ${WIFI_MODULE_IP} =     Get Wifi Ip
    ${GATEWAY_IP} =     Get Gateway Ip
    ${RET} =    Wait Until Device Is Pingable     ${GATEWAY_IP}
    Should Be True    ${RET}

Check for Wi-Fi Signal Strength with Threshold
     Log    Wi-Fi Signal Strength Threshold: ${SIGNAL_LEVEL_THRESHOLD}
     ${link}     ${level}     ${noise} =     Get Wifi Signal Quality
     Should Be True      ${level} >= ${SIGNAL_LEVEL_THRESHOLD}



