import subprocess
import re
import os
from os import mkdir
from os.path import isdir, join, isfile
from shutil import rmtree
from time import sleep
from shlex import split


class helper(object):
    """
    This is a helper file for sharing common
    function among different python files.

    Uses python-systemd wrapper module
    It requires: build-essential libsystemd-dev
    """

    def __init__(self):
        self._tmp_folder = "/tmp/test_lib/"

        if isdir(self._tmp_folder) is True:
            rmtree(self._tmp_folder)

        mkdir(self._tmp_folder)

    def cpu_core_validation(self, core):
        """
            Helper function to validate the cpu core arguments

            :param core: core number.
            :return Expection raised if the core number is invalid.
        """

        if not isinstance(core, int):
            s = "The value of core '{}' is not integer".format(core)
            raise TypeError(s)

        if (core >= self.get_physical_cores()) or (core < 0):
            s = "CPU Core == '{}' out of bounds".format(core)
            raise ValueError(s)

    def is_maschine_usb_detected(self):
        """
            Detects if Maschine MK3 HW controller or Maschine Standalone
            is recognized by the OS as a USB device.
            Relies on having 'lsusb' utility.

            :return : True or False.
        """

        supported_devices = ['17cc:1600', '17cc:1820']
        lsusb = self.execute_cmd_output_string('lsusb')

        for supported_device in supported_devices:
            if supported_device in lsusb:
                return True

        return False

    def is_maschine_alsa_detected(self):
        """
            Detects if Maschine MK3 Hw controller is recognized
            as a USB audio device by ALSA.
            Relies on having 'aplay' utility

            :return : True or False
        """

        aplay = self.execute_cmd_output_string('aplay -l')

        if 'MK3 [Maschine MK3], device 0: USB Audio [USB Audio]' in aplay:
            return True
        else:
            return False

    def is_integer_value(self, value):
        """
            Check if value type (instance object) is int.

            :param value : any value.
            :return : raise a TypeError exception if is not int. None, o.w.
        """

        if not isinstance(value, int):
            s = "The value of core '{}' is not integer".format(value)
            raise TypeError(s)

    def search_file(self, regex, filepath, line=None):
        """
            Funtion for finding regex pattern over a text file

            :param regex : compiled regex (e.g. re.compile())
            :param filepath : filepath to the target file
            :param line : if you want to find especific pattern in
                          especific line
            :return : a String if it is found, o.w. exception
        """

        with open(filepath) as f:
            if line:
                lines = f.readlines()
                return (regex.search(lines[line])).group()
            else:
                content = f.read()
                if regex.search(content) is None:
                    raise LookupError(
                        "Required data not found in {}"
                        .format(filepath)
                    )
                else:
                    return (regex.search(content)).group()

    def execute_cmd_output_file(self, cmd, filename, enable_shell=False):
        """
            Execute a command and send the standart output to a file.

            :param cmd: abs path of the command with arguments
            :param filename: filename of the file
            :param enable_shell : force the cmd to be run as shell script
            :return: filename path
        """

        logfile = join(self._tmp_folder, filename)

        with open(logfile, 'w') as f:
            try:
                result = subprocess.call(split(cmd), stdout=f,
                                         stderr=f, shell=enable_shell)

                if (result != 0):
                    raise AssertionError(
                        "Return code was not successful for {}"
                        .format(cmd))

            except Exception:
                raise AssertionError("While executing {} something went wrong"
                                     .format(cmd))

        return logfile

    def execute_cmd_output_string(self, cmd, enable_shell=False):
        """
            Execute a command and return its output as a string.

            :param cmd: abs path of the command with arguments
            :param enable_shell : force the cmd to be run as shell script
            :return: a string.
        """

        try:
            result = subprocess.check_output(split(cmd),
                                             stderr=subprocess.STDOUT,
                                             shell=enable_shell)

        except subprocess.CalledProcessError as e:
            s = """While executing '{}' something went wrong.
                Return code == '{}'
                Return output:\n'{}'
                """.format(cmd, e.returncode, e.output, shell=enable_shell)
            raise AssertionError(s)

        return result.strip().decode("utf-8")

    def execute_cmd_return_code(self, cmd, no_output=True, enable_shell=False):
        """
            Execute a command and return its exit code as a integer.

            :param cmd: abs path of the command with arguments.
            :param no_output: Output is printed or not.
            :param enable_shell : force the cmd to be run as shell script
            :return: a string.
        """

        if no_output is True:
            NULL = open(os.devnull, 'w')
            return subprocess.call(split(cmd), stdout=NULL,
                                   stderr=NULL, shell=enable_shell)
        else:
            return subprocess.call(cmd.split())

    def execute_ssh_output_list(self, ip, cmd):
        """
            Execute a SSH 'cmd' to a 'ip'.
            It returns the SSH command output as a list.

            :param ip : IP address
            :param cmd : a SSH command
            :return : a list
        """

        args = "-o StrictHostKeyChecking=no " \
               "-o UserKnownHostsFile=/dev/null " \
               "-i /home/root/.ssh/id_rsa_dtfb"

        ret = self.execute_cmd_output_string("ssh {} root@{} {}".format(args,
                                                                        ip,
                                                                        cmd))

        # removing warning line caused by SSH args.
        return ret.split("\n")[1:]

    def execute_ssh_return_code(self, ip, cmd):
        """
            Execute a SSH 'cmd' to a 'ip'.
            It returns the exit code.

            :param ip : IP address
            :param cmd : a SSH command
            :return : a integer
        """

        args = "-o StrictHostKeyChecking=no " \
               "-o UserKnownHostsFile=/dev/null " \
               "-i /home/root/.ssh/id_rsa_dtfb"

        ret = self.execute_cmd_return_code("ssh {} root@{} {}".format(args,
                                                                      ip,
                                                                      cmd))

        return ret

    def read_file_output_string(self, filepath):
        """
            Read a file and send its content as a string.

            :param filepath : filepath to the file.
            :return : a string.
        """

        if isfile(filepath) is False:
            e = "File '{}' not found".format(filepath)
            raise IOError(e)

        with open(filepath, 'r') as file:
            return file.read().strip()

    def is_ping_succeeded(self, ip, timeout=2):
        """
            Ping a device once and return if it succeeded or not.
            There is a default timeout == 2.

            :param ip : IP address
            :param timeout : pinging timeout
            :return : bool (True --> succeed. False otherwise)
        """

        exit_code = self.execute_cmd_return_code("ping -c 1 -w \
                                                 {} {}".format(timeout, ip))

        return True if exit_code == 0 else False

    def _calculate_count_arg(self, file_size, bs):
        """
            Helper to calculate count argument in dd to copy a file.

            :param file_size : string (e.g. 16M, 1m)
            :param bs : string (e.g. 128, 1M)

            :return an integer
        """

        file_size = str(file_size)
        bs = str(bs)

        if file_size[-1].isdigit() is True:
            # so filesize in bytes
            size = int(file_size)
        elif file_size[-1].lower() == 'k':
            # so filesize is kilobytes
            size = int(file_size[:-1]) * pow(2, 10)
        elif file_size[-1].lower() == 'm':
            # so filesize is megabytes
            size = int(file_size[:-1]) * pow(2, 20)
        else:
            raise Exception("File Size `{}` not supported".format(file_size))

        if bs[-1].isdigit() is True:
            # so filesize in bytes
            bs_size = int(bs)
        elif bs[-1].lower() == 'k':
            # so filesize is kilobytes
            bs_size = int(bs[:-1]) * pow(2, 10)
        elif bs[-1].lower() == 'm':
            # so filesize is megabytes
            bs_size = int(bs[:-1]) * pow(2, 20)
        else:
            raise Exception("bs `{}` not supported".format(bs))

        if (bs_size > size):
            raise Exception("bs size `{}` can be higher \
                             then file size `{}`".format(bs_size, size))

        return int(size // bs_size)

    def run_dd(self, in_fp, out_fp, in_fz, bs, args=''):
        """
            Wrapper for running ``dd`` on the Test Board.

            :param: in_fp == input filepath
            :param: out_fp == output filepath
            :param: in_fz == input filesize
            :param: bs == block size
            :param: args == args to be used in dd (e.g. 'oflag=nocache')

            :return : a string output of the dd cmd
        """

        count = self._calculate_count_arg(in_fz, bs)
        cmd = 'dd if={} of={} bs={} count={} {}'.format(in_fp, out_fp,
                                                        bs, count, args)
        return self.execute_cmd_output_string(cmd)

    def parsing_dd_output(self, dd_output):
        """
            To collect the speed and its units from the DD output.

            :param dd_output: a string output of the dd cmd
            :return: speed value and unit as tuple.
        """

        aux = dd_output.split()
        return aux[-2], aux[-1]

    def system_reboot_device(self, ip):
        """
            System reboot a device pointed by a IP.

            :param ip : IP Address
        """

        self.execute_ssh_return_code(ip, '/sbin/reboot')

    def system_shutdown_device(self, ip):
        """
            System shutdown a device pointed by a IP.

            :param ip : IP Address
        """

        self.execute_ssh_return_code(ip, '/sbin/poweroff')

    def hw_reset_device(self):
        """
            Hardware (forced) reset the target board connected to
            the test board through GPIO pins.
        """

        self.execute_cmd_return_code('gpio-tool.sh reset')

    def hw_poweroff_device(self):
        """
            Hardware (forced) poweroff the target board connected to
            the test board through GPIO pins.
        """

        self.execute_cmd_return_code('gpio-tool.sh poweroff')

    def hw_poweron_device(self):
        """
            Hardware (forced) poweron the target board connected to
            the test board through GPIO pins.
        """

        self.execute_cmd_return_code('gpio-tool.sh poweron')
        sleep(2)
        # for some reason it is necessary a reset cmd after poweron
        self.execute_cmd_return_code('gpio-tool.sh reset')

    def system_uptime(self, ip, arg):
        """
            System uptime pointed by a IP.
            arg == p --> pretty (e.g. 'up 2 minutes')
            arg == s --> since (e.g. '2018-07-12 10:30:54')

            :param ip : IP Address
            :param arg: argument (p or s)
            :return: a string or Exception
        """

        if arg == 's':
            return self.execute_ssh_output_list(ip, '/usr/bin/uptime -s')[0]
        elif arg == 'p':
            return self.execute_ssh_output_list(ip, '/usr/bin/uptime -p')[0]
        else:
            raise Exception("arg '{}' not valid".format(arg))

    def wait_until_device_is_pingable(self, ip, timeout=60):
        """
            Wait unit a device is pingable.
            It returns True if pingable until timeout False o.w.

            :param ip : IP Address
            :timeout : timeout (default=60 seconds)
            :return : boolean
        """

        # timeout/2 because is_ping_succedded takes 2s to complete
        for i in range(timeout // 2):
            ret = self.is_ping_succeeded(ip)
            if ret is True:
                return True

        return False

    def wait_until_device_is_not_pingable(self, ip, timeout=60):
        """
            Wait unit a device is not pingable.
            It returns True if not pingable until timeout False o.w.

            :param ip : IP Address
            :timeout : timeout (default=60 seconds)
            :return : boolean
        """

        # timeout/2 because is_ping_succedded takes 2s to complete
        for i in range(timeout // 2):
            ret = self.is_ping_succeeded(ip)
            if ret is False:
                return True

        return False

    def get_physical_cores(self, filename='cpuinfo'):
        """
            Get number of the CPU physical cores from cpuinfo.

            :param filename : Output filename to be store
            :return : integer value
        """

        filepath = '/proc/cpuinfo'

        cmd = 'cat {}'.format(filepath)
        logfile = self.execute_cmd_output_file(cmd, filename)
        regex = re.compile(r'(?<=cpu cores\s\:\s).*')

        return int(self.search_file(regex, logfile))

    def get_cpu_model(self, filename='cpuinfo'):
        """
            Get the CPU model from cpuinfo.

            :param filename : Output filename to be store
            :return : integer value
        """

        filepath = '/proc/cpuinfo'

        cmd = 'cat {}'.format(filepath)
        logfile = self.execute_cmd_output_file(cmd, filename)
        regex = re.compile(r'(?<=model\s\s:\s).*')

        return int(self.search_file(regex, logfile))

    def get_cpu_model_name(self, filename='cpuinfo'):
        """
            Get the CPU model name from cpuinfo.

            :param filename : Output filename to be store
            :return : string value
        """

        filepath = '/proc/cpuinfo'

        cmd = 'cat {}'.format(filepath)
        logfile = self.execute_cmd_output_file(cmd, filename)
        regex = re.compile(r'(?<=model name\s\:\s).*')

        return self.search_file(regex, logfile)

    def get_cpu_temp(self):
        """
            Get the CPU temperature in Celsius from the temp file.
            Kelnel docs:
            https://www.kernel.org/doc/Documentation/thermal/sysfs-api.txt

            :return: float number.
        """

        filepath = "/sys/class/thermal/thermal_zone0/temp"

        with open(filepath) as f:
            return float(f.readline()) / 1000

    def get_kernel_release(self):
        """
            Get the Kernel Release (e.g. '4.14.40-rt30-intel-pk-preempt-rt')

            :return: a string.
        """

        return self.execute_cmd_output_string("uname -r")

    def get_cpu_arch(self):
        """
            Get the CPU Archtecture (e.g. 'x86_64')

            :return: a string.
        """

        return self.execute_cmd_output_string("uname -m")

    def get_yocto_timestamp(self):
        """
            Get the Yocto build timestamp (e.g. '20180627115501')

            :return: a integer.
        """

        filepath = "/etc/version"

        return int(self.read_file_output_string(filepath))

    def get_bamboo_version(self):
        """
            Get the Bamboo build timestamp (e.g. '20180627115501')

            :return: a string.
        """

        filepath = "/etc/congatec-tca5-64_yocto_version"

        return self.read_file_output_string(filepath)
