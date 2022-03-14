import helper
import time

import robot.api.logger as logger

class Bt(object):
    """
        BT wrapper for Bluez hci tools utility.

        e.g.:

        root:~# hciconfig hci0 up
        root:~# hcitool dev
        Devices:
            hci0	18:1D:EA:83:C3:17
        root:~# hcitool scan
        Scanning ...
            20:47:DA:30:3A:3E	Redmi
            00:25:00:C6:FE:37	II-Mac
            64:A2:F9:06:63:79	OnePlus 6
            00:09:DF:EA:CC:16	MEDION TV
        root:~#
    """

    def __init__(self):
        self._helper = helper.helper()

###############################################################################
# BT METHODS
###############################################################################

    def bt_power(self):

        """Power on Bluetooth module."""

        cmd = "hciconfig hci0 up"
        exit_code = self._helper.execute_cmd_return_code(cmd)

    def bt_verify_interface(self):

        """
            Power on bluetooth module.

            Verify Bluetooth interface.

           :return: Return 'True' if 'hci0' interface is up or 'False' if 'hci0' interface is not up.
        """

        self.bt_power()

        cmd = "hcitool dev"
        ret = self._helper.execute_cmd_output_string(cmd)

        if 'hci0' in ret:
            return True

        return False

    def bt_parse_device_info(self, info_string):

        """Parse a string corresponding to a device."""

        res = info_string.split("\n", 2)

        try:
            if len(res[1]) > 1:
                ret = True
        except IndexError:
            ret = False

        return ret

    def bt_scan(self, timeout=20):
        """
            Check if bluetooth interface is up, Start bluetooth scanning process.

            :Log: device info by mac address and name.
        """

        exit_code = self.bt_verify_interface()

        if exit_code is True:

            cmd = "hcitool scan"

            for i in range(timeout):
                output = self._helper.execute_cmd_output_string(cmd)
                time.sleep(1)
                ret = self.bt_parse_device_info(output)
                if ret is True:
                    logger.info(str(output))
                    return True
                else:
                    return False

        return False



