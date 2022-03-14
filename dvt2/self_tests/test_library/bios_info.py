import helper


class bios_info(object):
    """
        Get Board/BIOS Information.

        e.g.:

            System BIOS Version:        QA50R131
            OEM BIOS Version:           UNKNOWN
            BC Firmware Version:        CGBCP428
            Board Name:                 QA50
            Board Sub Name:             QA50
            Product Revision:           A.1 (0x4131)
            Part Number:                015500
            EAN Code:                   04250186188528
            Serial Number:              000003382172
            Manufacturing Date:         2017.07.28
            Last Repair Date:           0000.00.00
            Boot Counter:               582
            CGOS API Version:           0x01030015
            CGOS Driver Version:        0x01020015
            Running Time:               3486 hours
            BIOS Write Protection:      Inactive

    """

    def __init__(self):
        self._helper = helper.helper()

###############################################################################
# BIOS INFORMATION METHODS
###############################################################################

    def get_system_oem_bios_version(self):
        """
            Get System BIOS and OEM BIOS version.

            e.g.:

                System BIOS Version:        QA50R131
                OEM BIOS Version:           UNKNOWN

                out[-2]                     QA50R131
                out[-1]                     UNKNOWN

            :return: command output as strings.
        """

        cmd = "/usr/bin/cgutlcmd CGINFO /OT:BOARD /DUMP /BIOS /SILENT"
        out = self._helper.execute_cmd_output_string(cmd).split("\n")
        return out[-2], out[-1]

    def get_bc_firmware_version(self):
        """
            Get board controller firmware version.

            e.g.:

                BC Firmware Version:        CGBCP428

                out[-1]                     CGBCP428

            :return: command output as string.
        """

        cmd = "/usr/bin/cgutlcmd CGINFO /OT:BOARD /DUMP /BCFW  /SILENT"
        out = self._helper.execute_cmd_output_string(cmd).split("\n")
        return out[-1]

    def get_cpu_manu_data(self):
        """
            Get CPU-board manufacturing data.

            e.g.:

                Board Name:                 QA50
                Board Sub Name:             QA50
                Product Revision:           A.1 (0x4131)
                Part Number:                015500
                EAN Code:                   04250186188528
                Serial Number:              000003382172
                Manufacturing Date:         2017.07.28
                Last Repair Date:           0000.00.00

                out[-8]                     QA50
                out[-7]                     QA50
                out[-6]                     A.1 (0x4131)
                out[-5]                     015500
                out[-4]                     04250186188528
                out[-3]                     000003382172
                out[-2]                     2017.07.28
                out[-1]                     0000.00.00

            :return: command output as strings.
        """

        cmd = "/usr/bin/cgutlcmd CGINFO /OT:BOARD /DUMP /MANU  /SILENT"
        out = self._helper.execute_cmd_output_string(cmd).split("\n")
        return out[-8], out[-7], out[-6], out[-5], out[-4], out[-3], out[-2], out[-1]

    def get_boot_counter(self):
        """
            Get Boot Counter.

            e.g.:

                Boot Counter:               582

                out[-1]                     582

            :return: command output as strings.
        """

        cmd = "/usr/bin/cgutlcmd CGINFO /OT:BOARD /DUMP /BCNT  /SILENT"
        out = self._helper.execute_cmd_output_string(cmd).split("\n")
        return out[-1]

    def get_cgos_interface_driver_version(self):
        """
            Get CGOS API and CGOS Driver Version.

            e.g.:

                CGOS API Version:           0x01030015
                CGOS Driver Version:        0x01020015

                out[-2]                     0x01030015
                out[-1]                     0x01020015

            :return: command output as strings.
        """

        cmd = "/usr/bin/cgutlcmd CGINFO /OT:BOARD /DUMP /CGOS  /SILENT"
        out = self._helper.execute_cmd_output_string(cmd).split("\n")
        return out[-2], out[-1]

    def get_running_time(self):
        """
            Get Running time in hours.

            e.g.:

                Running Time:               3486 hours

                out[-1]                     3486

            :return: command output as strings.
        """

        cmd = "/usr/bin/cgutlcmd CGINFO /OT:BOARD /DUMP /RTIM  /SILENT"
        out = self._helper.execute_cmd_output_string(cmd).split("\n")
        return out[-1]

    def get_bup_write_prot_data(self):
        """
            Get BIOS Write Protection status.

            e.g.:

                BIOS Write Protection:      Inactive

                out[-1]                     Inactive

            :return: command output as strings.
        """

        cmd = "/usr/bin/cgutlcmd CGINFO /OT:BOARD /DUMP /BUP  /SILENT"
        out = self._helper.execute_cmd_output_string(cmd).split("\n")
        return out[-1]

