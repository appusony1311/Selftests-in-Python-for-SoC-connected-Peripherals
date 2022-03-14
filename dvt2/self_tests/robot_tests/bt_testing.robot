*** Settings ***
Documentation          This is the Maschine Native OS Build Bluetooth Test.
...                    This is the minimun required for a build to be consided
...                    stable.
...                    ** This test suite must run in the TARGET board **
Library  ..${/}test_library${/}helper.py
Library  ..${/}test_library${/}Bt.py


*** Variables ***


*** Test Cases ***
Bluetooth Check for the Interface
    ${RET} =     Bt Verify Interface
    Should Be True    ${RET}

Bluetooth Scanned Devices
    ${RET} =     Bt Scan
    Should Be True    ${RET}


