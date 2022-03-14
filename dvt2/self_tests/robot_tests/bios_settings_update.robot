*** Settings ***
Documentation          This is the Maschine Native OS BIOS settings update.
...                    This is the minimun required for a build to be consided
...                    stable.
...                    ** This suite must run in the TARGET board **
Library  ..${/}test_library${/}helper.py
Library  ..${/}test_library${/}bios_settings_update.py

*** Variables ***
${BACKUP_MAP_FILE}         ${/}usr${/}share${/}congatec${/}bios-backup-map.mod
${DEFAULT_MAP_FILE}        ${/}usr${/}share${/}congatec${/}bios-default-map.mod
${WRITE_BACKUP_MAP}        1
${WRITE_DEFAULT_MAP}       2

*** Test Cases ***
Updating Backup Map file
     ${ret} =     Bios Settings Update    ${BACKUP_MAP_FILE}     ${WRITE_BACKUP_MAP}
     Should Be True    ${ret}
Updating Default Map file
     ${ret} =     Bios Settings Update    ${DEFAULT_MAP_FILE}    ${WRITE_DEFAULT_MAP}    
     Should Be True    ${ret}

