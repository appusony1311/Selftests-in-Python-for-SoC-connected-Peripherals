*** Variables ***
# general variables
${IP}                        10.1.9.42

# g_mass_storage variables
${REM_OTG_BLOB_SIZE}         512M
${REM_OTG_BLOB_PATH}         ${/}home${/}root${/}blob.bat
${REM_OTG_BLOB_MD5_PATH}     ${/}home${/}root${/}blob.md5
${LOC_OTG_BLOB_PATH}         ${TEMPDIR}${/}blob.bat
${LOC_OTG_BLOB_MD5_PATH}     ${TEMPDIR}${/}blob.md5
${LOC_OTG_PARTI_PATH}        sda

# g_ether variables
${REM_OTG_ETHER_IP}          192.168.0.20
${LOC_OTG_ETHER_IP}          192.168.0.21
