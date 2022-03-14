*** Settings ***
Documentation          This is the Maschine Native OS Build RAM Info Test.
...                    This is the minimun required for a build to be consided
...                    stable.
...                    ** This test suite must run in the TARGET board **
Library  ..${/}test_library${/}helper.py
Library  ..${/}test_library${/}ram_info.py


*** Variables ***
${RAM_SIZE}                 7990000

*** Test Cases ***
Get RAM Size - Total Memory and Free Memory (in KB).
     ${Total Memory}     ${Free Memory} =     Ram Info
     Log    Total Memory is ${Total Memory}
     Log    Free Memory is ${Free Memory}
     Should Be True      ${Total Memory}  >= ${RAM_SIZE}   # to avoid wrong measuraments.



