import helper
import os
import time

import robot.api.logger as logger



class wifi(object):
    """
        WIFI setters and getters.
    """

    def __init__(self):
        self._helper = helper.helper()

###############################################################################
# Wi-Fi METHODS
###############################################################################

    def wifi_enable(self, option, timeout=20):
        """
            Enable wifi if option is "up" and disable if option is "down".

            param ip : IP Address.
            :timeout : timeout (default=20 seconds).
            :return: command output as True or False.
        """

        cmd = "nmcli radio wifi %s" % option

        for i in range(timeout):
            exit_code = self._helper.execute_cmd_return_code(cmd)
            time.sleep(1)
            if exit_code == 0:
                return True

        return False

    def wifi_list_accesspoints(self):
        """
            List Wi-Fi Access points.

            :log: command output as strings (list of Access point names).
        """

        cmd = "nmcli -t -f SSID dev wifi list"
        ret = self._helper.execute_cmd_output_string(cmd)
        time.sleep(3)
        logger.info(str(ret))

    def wifi_disconnect(self, ssid, timeout=20):
        """
            Disconnect from current network connection.

            :timeout : timeout (default=20 seconds).
            :return: command output as True or False.
        """

        cmd = "nmcli device disconnect wlp1s0"
        self._helper.execute_cmd_return_code(cmd)

        cmd = "nmcli device set wlp1s0 autoconnect no"
        self._helper.execute_cmd_return_code(cmd)

        cmd = "nmcli c mod  '%s' connection.autoconnect no" % ssid
        self._helper.execute_cmd_return_code(cmd)

        cmd = "nmcli -t -f TYPE,UUID con"
        res = self._helper.execute_cmd_output_string(cmd)
        lines = res.split("\n")

        for line in lines:
            parts = line.split(":")
            if parts[0] == "802-11-wireless":
                cmd = "nmcli connection delete uuid '%s'" % parts[1]
                for i in range(timeout):
                    exit_code = self._helper.execute_cmd_return_code(cmd)
                    time.sleep(1)
                    if exit_code == 0:
                        return True

        return False

    def wifi_connect(self, ssid, pw, timeout=30):
        """
            Connect to Access point using SSID and PW.

            :param ssid: SSID of the ACCESS POINT.
            :param pw: password for connecting to the access point.
            :timeout : timeout (default=30 seconds).
            :return: command output as True or False.
        """

        cmd = "nmcli device wifi connect '%s' password '%s'" % (ssid, pw)
        for i in range(timeout):
            exit_code = self._helper.execute_cmd_return_code(cmd)
            time.sleep(1)
            if exit_code == 0:
                return True

        return False

    def wifi_disconnect_then_connect(self, ssid, pw):
        """
            Disable and enable to reset the Wi-Fi Module to avoid if Wi-Fi Module is not initialized correctly.
            Disconnect from current network configuration.
            Connect to the SSID and PW passed as arguments 'ssid' and 'pw'.

            :param ssid: SSID of the ACCESS POINT.
            :param pw: password for connecting to the access point.
            :return: command output as True or False.
        """

        exit_code = self.wifi_enable("off")

        exit_code = self.wifi_enable("on")

        self.wifi_disconnect(ssid)

        self.wifi_connect(ssid, pw)

        exit_code = self.wifi_connect_verify()

        if exit_code is True:
            return True

        return False

    def wifi_connect_verify(self, timeout=20):
        """
            Verify Connectivity of WIFI module to the Access Point.

            :timeout : timeout (default=20 seconds).
            :return: command output as True or False.
        """

        filepath = "/sys/class/net/wlp1s0/operstate"

        for i in range(timeout):
            ret = self._helper.read_file_output_string(filepath)
            time.sleep(1)
            if 'up' in ret:
                return True

        return False

    def get_wifi_ip(self):
        """
            Get the IP address to the WIFI module from the Access Point.
        """

        cmd = '/sbin/ifconfig wlp1s0 | grep "inet addr" | cut -d: -f2 | cut -d" " -f1'
        f = os.popen(cmd)
        return f.read().strip()

    def get_gateway_ip(self):
        """
            Get the Gateway IP address of the Access Point.

            :return: Gateway IP.
        """

        cmd = '/sbin/ifconfig wlp1s0 | grep "inet addr" | cut -d: -f2 | cut -d" " -f1'
        f = os.popen(cmd)
        ip_address = f.read().strip()

        list_ = ip_address.split('.')
        assert len(list_) == 4
        list_[3] = '1'

        return '.'.join(list_)

    def median(self, lst):
        n = len(lst)
        if n < 1:
            return None
        if n % 2 == 1:
            return sorted(lst)[n // 2]
        else:
            return sum(sorted(lst)[n // 2 - 1:n // 2 + 1]) / 2.0

    def get_wifi_signal_quality(self):
        """
            Get the Wi-Fi signal quality related params link, level and noise.

            :return: median of link, level, and noise (as integers).
        """

        linkList = []
        levList = []
        noiseList = []

        # start timer
        startTime = time.time()
        for i in range(0,10):

            # get time stamp
            thisTime = time.time() - startTime

            with open("/proc/net/wireless", "r") as f:
                data = f.read()

            linkList.append(int(data[177:179]))
            levList.append(int(data[182:185]))
            noiseList.append(int(data[187:192]))

            # wait for next timer
            while ((time.time() - startTime) - thisTime < .5):
                pass

        link = int(self.median(linkList))
        level = int(self.median(levList))
        noise = int(self.median(noiseList))

        return link, level, noise
