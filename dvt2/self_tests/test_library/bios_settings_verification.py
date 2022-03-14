import helper


class bios_settings_verification(object):
    """
        The BIOS Settings verification Wrapper code for verifying updated BIOS default and backup map.
    """

    def __init__(self):
        self._helper = helper.helper()

###############################################################################
# BIOS SETTINGS VERIFICATION METHOD
###############################################################################

    def bios_settings_verification(self, map_file, option):
        """
            Verify the BIOS settings from the map file and with the option as the argument.

            :param map_file: BIOS Settings MAP.
            :param option: Option is '1' for comparing backup map and '2' for default map.
            :return: command output as True or False.
        """

        cmd = "/usr/bin/cgutlcmd MODULE /OT:BOARD /CMP /IF:%s /T:%s" % (map_file, option)
        exit_code = self._helper.execute_cmd_return_code(cmd)

        return exit_code == 0




