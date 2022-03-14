import helper


class bios_settings_update(object):
    """
        BIOS Settings update.

        OBS: The BIOS Settings Update Wrapper code for updating default and backup map.
    """

    def __init__(self):
        self._helper = helper.helper()

###############################################################################
# BIOS SETTINGS UPDATE METHOD
###############################################################################

    def bios_settings_update(self, map_file, option):
        """
            Update the BIOS settings from the map file and with the option as the argument.

            :param map_file: BIOS Settings MAP.
            :param option: Option is '1' for writing backup map and '2' for default map.
            :return: command output as True or False.
        """

        cmd = "/usr/bin/cgutlcmd MODULE /OT:BOARD /ADD /IF:%s /T:%s" % (map_file, option)
        exit_code = self._helper.execute_cmd_return_code(cmd)

        return True if exit_code == 0 else False




