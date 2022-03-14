import helper


class cpufreq(object):
    """
        cpufreq getters and setters
        info: https://www.kernel.org/doc/Documentation/cpu-freq/user-guide.txt
    """

    def __init__(self):
        self._helper = helper.helper()

###############################################################################
#                                      Getters
###############################################################################
    def get_cpufreq_cur_freq(self, core):
        """
            Get the current cpu frequency from cpufreq
            for a core (e.g. '2530').

            :param core: core number (e.g. 0)
            :return: cpu frequency in Mhz (integer).
        """

        self._helper.cpu_core_validation(core)

        filepath = '/sys/devices/system/cpu/cpu{}/' \
                   'cpufreq/cpuinfo_cur_freq'.format(core)

        return int(self._helper.read_file_output_string(filepath)) // 1000

    def get_cpufreq_min_freq(self, core):
        """
            Get the min cpu frequency from cpufreq
            for a core (e.g. '2530').

            :param core: core number (e.g. 0)
            :return: cpu frequency in Mhz (integer).
        """

        self._helper.cpu_core_validation(core)

        filepath = '/sys/devices/system/cpu/cpu{}/' \
                   'cpufreq/cpuinfo_min_freq'.format(core)

        return int(self._helper.read_file_output_string(filepath)) // 1000

    def get_cpufreq_max_freq(self, core):
        """
            Get the min cpu frequency from cpufreq
            for a core (e.g. '2530').

            :param core: core number (e.g. 0)
            :return: cpu frequency in Mhz (integer).
        """

        self._helper.cpu_core_validation(core)

        filepath = '/sys/devices/system/cpu/cpu{}/' \
                   'cpufreq/cpuinfo_max_freq'.format(core)

        return int(self._helper.read_file_output_string(filepath)) // 1000

    def get_scaling_available_governors(self, core):
        """
            Get the scaling available governors from cpuinfo
            for a core (e.g. 'performance powersave').

            :param core: core number (e.g. 0)
            :return: list of strings.
        """

        self._helper.cpu_core_validation(core)

        filepath = '/sys/devices/system/cpu/cpu{}/' \
                   'cpufreq/scaling_available_governors'.format(core)

        return self._helper.read_file_output_string(filepath).split()

    def get_scaling_driver(self, core):
        """
            Get the scaling driver name from cpuinfo
            for a core (e.g. 'intel_pstate').

            :param core: core number (e.g. 0).
            :return: a string.
        """

        self._helper.cpu_core_validation(core)

        filepath = '/sys/devices/system/cpu/cpu{}/' \
                   'cpufreq/scaling_driver'.format(core)

        return self._helper.read_file_output_string(filepath)

    def get_scaling_governor(self, core):
        """
            Get the current scaling governor name from cpuinfo
            for a core (e.g. 'performance powersave').

            :param core: core number (e.g. 0).
            :return: a string.
        """

        self._helper.cpu_core_validation(core)

        filepath = '/sys/devices/system/cpu/cpu{}/' \
                   'cpufreq/scaling_governor'.format(core)

        return self._helper.read_file_output_string(filepath)

    def get_scaling_max_freq(self, core):
        """
            Get the max scaling cpu frequency from cpuinfo
            for a core (e.g. '2530').

            :param core: core number (e.g. 0).
            :return: cpu frequency in Mhz (integer).
        """

        self._helper.cpu_core_validation(core)

        filepath = '/sys/devices/system/cpu/cpu{}/' \
                   'cpufreq/scaling_max_freq'.format(core)

        return int(self._helper.read_file_output_string(filepath)) // 1000

    def get_scaling_min_freq(self, core):
        """
            Get the min scaling cpu frequency from cpuinfo
            for a core (e.g. '2530').

            :param core: core number (e.g. 0).
            :return: cpu frequency in Mhz (integer).
        """

        self._helper.cpu_core_validation(core)

        filepath = '/sys/devices/system/cpu/cpu{}/' \
                   'cpufreq/scaling_min_freq'.format(core)

        return int(self._helper.read_file_output_string(filepath)) // 1000

    def get_scaling_cur_freq(self, core):
        """
            Get the current scaling cpu frequency from cpuinfo
            for a core (e.g. '2530').

            :param core: core number (e.g. 0).
            :return: cpu frequency in Mhz (integer).
        """

        self._helper.cpu_core_validation(core)

        filepath = '/sys/devices/system/cpu/cpu{}/' \
                   'cpufreq/scaling_cur_freq'.format(core)

        return int(self._helper.read_file_output_string(filepath)) // 1000

###############################################################################
#                                      Setters
###############################################################################
    def set_scaling_governor(self, core, governor):
        """
            Set the scaling governor for the spefic core.
            OBS: By design, this method do not verify if the governor is one of
            the scaling_available_governors. You should verify after setting.

            :param core : core number (e.g. 0)
            :param governor : governor name.
            :return if the governor is invalid, it throws a IOError.
        """

        self._helper.cpu_core_validation(core)

        filepath = '/sys/devices/system/cpu/cpu{}/' \
                   'cpufreq/scaling_governor'.format(core)

        with open(filepath, 'w') as file:
            file.write(governor)

    def set_scaling_max_freq(self, core, freq):
        """
            Set the scaling max frequency in Mhz for the spefic core.

            :param core : core number (e.g. 0).
            :param freq : frequency in Mhz
        """

        self._helper.cpu_core_validation(core)
        self._helper.is_integer_value(freq)

        filepath = '/sys/devices/system/cpu/cpu{}/' \
                   'cpufreq/scaling_max_freq'.format(core)

        with open(filepath, 'w') as file:
            # converting the Mhz value to kHz value
            file.write(str(freq * 1000))

    def set_scaling_min_freq(self, core, freq):
        """
            Set the scaling min frequency in Mhz for the spefic core.

            :param core : core number (e.g. 0).
            :param freq : frequency in Mhz
        """

        self._helper.cpu_core_validation(core)
        self._helper.is_integer_value(freq)

        filepath = '/sys/devices/system/cpu/cpu{}/' \
                   'cpufreq/scaling_min_freq'.format(core)

        with open(filepath, 'w') as file:
            # converting the Mhz value to kHz value
            file.write(str(freq * 1000))

    def set_scaling_cur_freq(self, core, freq):
        """
            Set the scaling cur frequency in Mhz for the spefic core.

            :param core : core number (e.g. 0).
            :param freq : frequency in Mhz.
        """

        self._helper.cpu_core_validation(core)
        self._helper.is_integer_value(freq)

        filepath = '/sys/devices/system/cpu/cpu{}/' \
                   'cpufreq/scaling_cur_freq'.format(core)

        with open(filepath, 'w') as file:
            # converting the Mhz value to kHz value
            file.write(str(freq * 1000))
