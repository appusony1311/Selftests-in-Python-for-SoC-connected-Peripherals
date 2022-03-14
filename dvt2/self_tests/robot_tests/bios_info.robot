*** Settings ***
Documentation          This is the Maschine Native OS Build BIOS Info Test.
...                    This is the minimun required for a build to be consided
...                    stable.
...                    ** This test suite must run in the TARGET board **
Library  ..${/}test_library${/}helper.py
Library  ..${/}test_library${/}bios_info.py


*** Variables ***


*** Test Cases ***
Get System BIOS and OEM BIOS version.
     ${system_bios_ver}     ${oem_bios_ver} =     Get System Oem Bios Version
     Log    System BIOS version is ${system_bios_ver}
     Log    OEM BIOS version is ${oem_bios_ver}

Get board controller firmware version.
     ${bc_firmware_ver} =     Get Bc Firmware Version
     Log    BC Firmware Version is ${bc_firmware_ver}

Get CPU-board manufacturing data.
     ${board_name}     ${board_sub_name}     ${prod_rev}     ${part num}     ${ean_code}     ${serial_num}     ${manu_date}     ${last_repair_date} =     Get Cpu manu data
     Log    Board Name is ${board_name}
     Log    Board Sub Name is ${board_sub_name}
     Log    Product Revision is ${prod_rev}
     Log    Part Number is ${part num}
     Log    EAN Code is ${ean_code}
     Log    Serial Number is ${serial_num}
     Log    Manufacturing Date is ${manu_date}
     Log    Last Repair Date is ${last_repair_date}

Get Boot Counter.
    ${boot_ctr} =    Get Boot Counter
    Log     Boot Counter is ${boot_ctr}

Get CGOS API and CGOS Driver Version.
     ${cgos_api_ver}     ${cgos_driver_ver} =     Get Cgos Interface Driver Version
     Log    CGOS API Version is ${cgos_api_ver}
     Log    CGOS Driver Version is ${cgos_driver_ver}

Get Running time in hours.
    ${running_time} =    Get Running Time
    Log     Running Time is ${running_time}

Get BIOS Write Protection status.
    ${bios_write_prot_stat} =    Get Bup Write Prot Data
    Log     BIOS Write Protection is ${bios_write_prot_stat}



