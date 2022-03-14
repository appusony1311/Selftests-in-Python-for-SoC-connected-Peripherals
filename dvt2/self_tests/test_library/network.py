import helper
from os import popen
from json import load


class network(object):
    """
        Network methods for testing.
        This tests should be running on the Test Board

        OBS: The iperf3 code must be rewrite, because there is iperf3 API
        `libiperf`. Also, there is already a iperf3 wrapper available. I wrote
        this not being awared about it. My fault.
        https://pypi.org/project/iperf3/
    """

    def __init__(self):
        self._helper = helper.helper()

###############################################################################
# REMOTE METHODS
###############################################################################
    def start_remote_iperf3_server(self, ip, args=''):
        """
            Start a remote iperf3 server as a deamon. More args can be used.

            :param ip: Target IP.
            :param args: More arguments can be included here.
            :return: the SSH output as a list.
        """

        cmd = "iperf3 -s -D %s" % args
        return self._helper.execute_ssh_output_list(ip, cmd)

    def is_remote_iperf3_server_running(self, ip):
        """
            Check if a remote iperf3 server is running in the target board.

            :param ip: Target IP.
            :return: a boolean value.
        """

        # getting iperf3 pids
        cmd = "ps aux | grep iperf3 | awk '{print $2}'"
        pids = self._helper.execute_ssh_output_list(ip, cmd)

        # ugly but it works... avoind installing dependencies!
        return True if len(pids) == 3 else False

    def kill_remote_iperf3_server(self, ip):
        """
            Kills any remote iperf3 server to the target ip.

            :param ip: Target IP.
            :return: the SSH output as a list.
        """

        cmd = 'killall iperf3'
        return self._helper.execute_ssh_output_list(ip, cmd)

###############################################################################
# LOCAL METHODS
###############################################################################
    def start_iperf3_server(self, args=''):
        """
            Start a local iperf3 server as a demon. More args can be used.

            :param args: More arguments can be included here.
            :return: command output as string.
        """

        cmd = "iperf3 -s -D %s" % args
        return self._helper.execute_cmd_output_string(cmd)

    def start_iperf3_client(self, server_ip, filename, args=''):
        """
            Start a local iperf3 client targeting the `server_ip`.
            It outputs the client output in a json file pointed by 'filename'.
            More args can be used.

            :param args: More arguments can be included here.
            :return: json filepath.
        """

        cmd = "iperf3 -c {} {}".format(server_ip, args)
        return self._helper.execute_cmd_output_file(cmd, filename)

    def is_iperf3_server_running(self):
        """
            Check if a local iperf3 server is running.

            :return: a boolean value.
        """

        # getting iperf3 pids
        cmd = "ps aux | grep iperf3 | awk '{print $2}'"
        pids = popen(cmd).read().split()

        # ugly but it works... avoind installing dependencies!
        return True if len(pids) == 3 else False

    def kill_iperf3_server(self):
        """
            Kills any local iperf3 server.

            :return: the command output as a stirng.
        """

        cmd = 'killall iperf3'
        return self._helper.execute_cmd_output_string(cmd)

###############################################################################
# LOCAL METHODS
###############################################################################
    def decode_iperf3_json(self, filepath):
        """
            Deserialize a JSON file.

            :param filepath: JSON filepath.
            :return: a dictionary object.
        """

        return load(open(filepath, 'r'))

    def get_iperf3_sent_summary(self, iperf3_dict):
        """
            Get the iperf3 sent summary from a dictionary object
            (from decode_iperf_json).

            :param iperf3_dict: a dictionary object.
            :return: a sent summary dictionary.
        """

        sum_sent = iperf3_dict["end"]["sum_sent"]
        sum_sent["mb"] = int(sum_sent.get("bytes") / (2 ** 20))
        sum_sent["mb_per_second"] = \
            int(sum_sent.get("bits_per_second") / (2 ** 20))

        return sum_sent

    def get_iperf3_recv_summary(self, iperf3_dict):
        """
            Get the iperf3 received summary from a dictionary object
            (from decode_iperf_json).

            :param iperf3_dict: a dictionary object.
            :return: a sent summary dictionary.
        """

        sum_recv = iperf3_dict["end"]["sum_received"]
        sum_recv["mb"] = int(sum_recv.get("bytes") / (2 ** 20))
        sum_recv["mb_per_second"] = \
            int(sum_recv.get("bits_per_second") / (2 ** 20))

        return sum_recv
