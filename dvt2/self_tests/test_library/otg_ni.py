import helper
import os
from os.path import abspath
from time import sleep


class otg_ni(object):
    """
        Class to manipulate the OTG feature of our boards.

        Documentation:
        https://www.kernel.org/doc/Documentation/usb/mass-storage.txt
        http://www.linux-usb.org/gadget/file_storage.html

        =======
        SET UP
        =======
        For ``Congatec QEVA2`` board:

        In the HW board:
        - set jumper  X37: 1-2
        - SW9, position 4: On

        In BIOS:
        - Chipset > South Cluster Configuration > USB Configuration >
        > XDCI Support  [PCI mode]
        - Chipset > Platform Controller Hub (PCH) > OS Selection  [Intel Linux]

        Run method ``setup_remote_congatec_qeva2_g_multi``
   """

    def __init__(self):
        self._helper = helper.helper()

    ###########################################################################
    # TEST BOARD METHODS
    ###########################################################################
    def get_md5sum(self, filepath):
        """
            Calculates and get a md5sum of a local file.

            :param: filepath --> the filepath location.
            :return a md5sum string
        """

        with open(filepath, 'r') as file:
            return file.readline()

    def calc_md5_out_file(self, in_fp, out_fp):
        """
            Calculates a md5sum of local in_file and stores in the out_file.

            :param in_fp : Filepath to be calcuted.
            :param out_fp : Filepath to be stored the md5sum info.
        """

        cmd = 'md5sum {}'.format(abspath(in_fp))
        out = self._helper.execute_cmd_output_string(cmd).split()[0]

        with open(abspath(out_fp), 'w') as file:
            file.write(out)

    def is_fsg_present(self, disk_name='sda'):
        """
            Verify if the test board is seeing the File Storage Gadget
            from the target board. Returns True of False.

            :param disk_name: the partition name of the OTG from the board.
        """

        ret = self._helper.execute_cmd_output_string('lsblk')
        if disk_name in ret:
            return True

        return False

    def set_otg_ether_ip(self, ether_ip):
        """
            Set an IP address to the Ethernet over USB module
            in the test board.
        """

        cmd = '/sbin/ifconfig usb0 {}'.format(ether_ip)
        return self._helper.execute_cmd_output_string(cmd)

    def get_otg_ether_ip(self):
        """
            Get the IP address to the Ethernet over USB module
            in the test board.
        """

        cmd = 'ifconfig usb0 | grep "inet addr" | cut -d: -f2 | cut -d" " -f1'
        # using popen directly because some parsing issues this code the
        # execute_cmd_output_string method.
        f = os.popen(cmd)
        return f.read().strip()

    ###########################################################################
    # REMOTE METHODS (Q7 Boards)
    ###########################################################################
    def setup_remote_congatec_qeva2_g_multi(self, ip, filepath):
        """
            Setup the congatec board.

            :param ip: Target IP address.
            :param filepath: Point to g_multi to be shared.
            :return: returns the SSH output.
        """

        cmds = ['echo peripheral > \
                /sys/bus/platform/devices/intel-mux-drcfg/portmux.0/state',
                '/sbin/modprobe dwc3',
                '/sbin/modprobe dwc3_pci',
                '/sbin/modprobe libcomposite',
                '/sbin/modprobe g_multi file={}'.format(filepath)]

        for cmd in cmds:
            self._helper.execute_ssh_output_list(ip, cmd)
            sleep(1)

    def is_remote_otg_g_multi_enabled(self, ip):
        """
            Verify if the g_multi is enabled.

            :param ip : Target IP address
            :return: a bolean value.
        """

        strs_to_find = ['g_multi', 'dwc3', 'dwc3_pci', 'libcomposite']
        out = self._helper.execute_ssh_output_list(ip,
                                                   "lsmod | \
                                                   awk '{print $1}'")
        if all(x in out for x in strs_to_find):
            return True

        return False

    def enable_remote_otg_g_multi_ip(self, ip, ether_ip):
        """
            Set a IP address to the Ethernet over USB module
            in the target.

            :param ip : Target IP address
            :param ether_ip: Ether IP for the OTG module
            :return: a list with the SSH output.
        """

        cmds = ['/sbin/ifconfig usb0 up',
                '/sbin/ifconfig usb0 {}'.format(ether_ip)]

        for cmd in cmds:
            self._helper.execute_ssh_output_list(ip, cmd)
            sleep(1)

    def get_remote_otg_g_multi_ip(self, ip):
        """
            Get the IP address to the Ethernet over USB module
            in the target.

            :param ip : Target IP address
            :return: a list with the SSH output.
        """

        cmd = '/sbin/ifconfig usb0 | grep "inet addr" \
              | cut -d: -f2 | cut -d" " -f1'
        return self._helper.execute_ssh_output_list(ip, cmd)[0]

    def disable_remote_otg_g_multi(self, ip):
        """
            Disable OTG g_multi module on the host [Q7 module].
            Run in the host locally.

            :param ip : Target IP address
            :return a list with the SSH output.
        """

        cmd = '/sbin/modprobe -r g_multi'
        return self._helper.execute_ssh_output_list(ip, cmd)

    def calc_remote_md5sum(self, ip, blob_path, md5_path):
        """
            Calculates the md5sum of the `blob_path` file in the target
            and saves it on the `md5_path.

            :param ip : Target IP address.
            :param blob_path : File to be used on the OTG.
            :param md5_path : MD5sum file location on the target.
            :return: returns the SSH output.

        """

        cmd = '/usr/bin/md5sum {} > {}'.format(blob_path, md5_path)
        return self._helper.execute_ssh_output_list(ip, cmd)

    def get_remote_md5sum(self, ip, filepath):
        """
            Get the MD5sum of a file previous stored in the target board
            on the `filepath` location.

            :param ip : Target IP address.
            :param filepath : MD5sum file location on the target.
            :return: returns the SSH output.
        """

        cmd = 'cat {}'.format(filepath)
        return self._helper.execute_ssh_output_list(ip, cmd)[0].split()[0]

    def run_remote_dd(self, ip, in_fp, out_fp, in_fz, bs, args=''):
        """
            Wrapper for running ``dd`` on the Target.

            :param ip : Target IP address
            :param in_fp == input filepath
            :param out_fp == output filepath
            :param in_fz == input filesize
            :param bs == byte size for the dd
            :param args == args to be used in dd (e.g. 'oflag=nocache')

            :return: a list with the SSH output
        """

        count = self._helper._calculate_count_arg(in_fz, bs)
        cmd = 'dd if={} of={} bs={} count={} {}'.format(in_fp, out_fp,
                                                        bs, count, args)
        return self._helper.execute_ssh_output_list(ip, cmd)
