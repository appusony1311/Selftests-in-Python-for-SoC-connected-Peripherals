import helper
import os
from time import sleep


class sd(object):
    """
        sd getters and setters
        info: https://www.kernel.org/doc/Documentation/cpu-freq/user-guide.txt
    """

    def __init__(self):
        self._helper = helper.helper()

###############################################################################
# SD METHODS
###############################################################################

    def _clean_caches(self):

        cmd = "sync"
        self._helper.execute_cmd_output_string(cmd)
        with open("/proc/sys/vm/drop_caches", "w") as f:
            f.write("3")

    def _convert_sectors_in_megabytes(self, sectors, byte_sector):
        """
            Convert sectors in size (megabytes)

        :param sectors: number of sectors
        :param byte_sector: bytes for each sector (e.g. 512
        :return: megabyte value as integer
        """

        return int((sectors * byte_sector) / (2 ** 20))

    def get_sd_size(self):
        """
            Get the current sd size as integer.

            :return: sd size in megabytes.
        """

        filepath = "/sys/class/block/mmcblk0/size"
        sectors = int(self._helper.read_file_output_string(filepath))
        return self._convert_sectors_in_megabytes(sectors, 512)

    def get_sd_serial_num(self):
        """
            Get the current sd serial number.

            :return: sd serial number in strings.
        """

        filepath = "/sys/block/mmcblk0/device/serial"
        return self._helper.read_file_output_string(filepath)

    def get_sd_name(self):
        """
            Get the current sd name.

            :return: sd serial number in strings.
        """

        filepath = "/sys/block/mmcblk0/device/name"
        return self._helper.read_file_output_string(filepath)

    def is_mount_point_exists(self, mount_point):
        """
            Check whether mount point exists or not.

            :mount_point: Names of the mount_point path
            :return: True or False
        """

        return os.path.ismount(mount_point)  # returns boolean

    def get_size_of_mounted_partition(self, partition_name):
        """
            Get the size of the mounted partition.

            :partition_name : Partition Name as string (e.g. mmcblk0p1)
            :return: size of the mounted partition in megabytes as integer.
        """

        filepath = "/sys/class/block/{}/size".format(partition_name)
        sectors = int(self._helper.read_file_output_string(filepath))
        return self._convert_sectors_in_megabytes(sectors, 512)

    def get_fstype_of_mounted_partition(self, partition_path):
        """
            Get the filesystem type of the mounted partition.

            :partition_name : Partition path as string (e.g. /dev/mmcblk0p1)
            :return: filesystem type as string
        """

        cmd = "lsblk %s -n -o FSTYPE" % partition_path
        return self._helper.execute_cmd_output_string(cmd)

    def write_perf(self, in_fp, out_fp, in_fz, bs):
        """
            Get the write speed of sd.

            :param: in_fp == input filepath
            :param: out_fp == output filepath
            :param: in_fz == input filesize
            :param: bs == block size
            :param: args == args to be used in dd (e.g. 'oflag=nocache')

            :return : a string output of the dd cmd
        """
        self._clean_caches()
        sleep(1)
        dd_output = self._helper.run_dd(in_fp, out_fp,
                                        in_fz, bs,
                                        args='iflag=nocache oflag=nocache')

        return self._helper.parsing_dd_output(dd_output)

    def read_perf(self, in_fp, out_fp, in_fz, bs):
        """
            Get the read speed of sd.

            :param: in_fp == input filepath
            :param: out_fp == output filepath
            :param: in_fz == input filesize
            :param: bs == block size
            :param: args == args to be used in dd (e.g. 'oflag=nocache')

            :return : a string output of the dd cmd
        """
        self._clean_caches()
        sleep(1)
        dd_output = self._helper.run_dd(in_fp, out_fp,
                                        in_fz, bs,
                                        args='iflag=nocache oflag=nocache')

        return self._helper.parsing_dd_output(dd_output)
