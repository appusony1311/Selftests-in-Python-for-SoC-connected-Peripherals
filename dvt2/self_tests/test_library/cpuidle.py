import helper
from os import listdir


class cpuidle(object):
    """
        Class to get / set configuration & information from cpuidle subsystem.
        More info:
        * https://www.kernel.org/doc/Documentation/cpuidle/sysfs.txt
        * https://lwn.net/Articles/384146/
        * https://software.intel.com/en-us/articles/power \
          management-states-p-states-c-states-and-package-c-states
        * https://www.thomas-krenn.com/en/wiki/Processor_P-states_and_C-states
    """

    def __init__(self, cpuinfopath=None):
        self._helper = helper.helper()

    def _cpuidle_state_validation(self, core, state):
        """
            Verification if the state value is valid.

            :param core : core number (e.g. 0).
            :param state: a state level (e.g. 2).
        """

        state_levels = self.get_cpuidle_state_levels(core)
        assert isinstance(state, int)
        assert (state >= 0 and state < state_levels) is True

###############################################################################
#                                      Getters
###############################################################################
    def get_cpuidle_cur_driver(self):
        """
            Get the current cpuidle driver.

            :return : a string
        """

        filepath = '/sys/devices/system/cpu/cpuidle/current_driver'
        return self._helper.read_file_output_string(filepath)

    def get_cpuidle_cur_governor(self):
        """
            Get the current cpuidle governor.

            :return : a string
        """

        filepath = '/sys/devices/system/cpu/cpuidle/current_governor_ro'
        return self._helper.read_file_output_string(filepath)

    def get_cpuidle_state_levels(self, core=0):
        """
            Get number of cstates of a 'core'

            :param core: core number (e.g. 0)
            :return: a int value.
        """

        self._helper.cpu_core_validation(core)
        dirpath = '/sys/devices/system/cpu/cpu{}/cpuidle'.format(core)

        return len(listdir(dirpath))

    def get_cpuidle_state_info(self, info, core, state):
        """
            Get the idle state info based on info, core, state arguments.

            info:
            * desc : Small description about the idle state (string)
            * disable : Option to disable this idle state (bool)
            * latency : Latency to exit out of this idle state (in us)
            * residency : Time after which a state becomes more
                          effecient than any shallower state (in us)
            * name : Name of the idle state (string)
            * power : Power consumed while in this idle state (in milliwatts)
            * time : Total time spent in this idle state (in microseconds)
            * usage : Number of times this state was entered (count)

            :param info : file to be read. Valid values are:
            :param core : core number (e.g. 0).
            :param state: a state level (e.g. 2).
            :return : a string value.
        """

        self._helper.cpu_core_validation(core)
        self._cpuidle_state_validation(core, state)

        valid_info = ['desc', 'disable', 'latency', 'name', 'power',
                      'residency', 'time', 'usage']

        if info not in valid_info:
            raise Exception("Info '{}' not supported".format(info))
        elif info == 'desc':
            filepath = '/sys/devices/system/cpu/cpu' \
                       '{}/cpuidle/state{}/desc'.format(core, state)
        elif info == 'disable':
            filepath = '/sys/devices/system/cpu/cpu' \
                       '{}/cpuidle/state{}/disable'.format(core, state)
        elif info == 'latency':
            filepath = '/sys/devices/system/cpu/cpu' \
                       '{}/cpuidle/state{}/latency'.format(core, state)
        elif info == 'name':
            filepath = '/sys/devices/system/cpu/cpu' \
                       '{}/cpuidle/state{}/name'.format(core, state)
        elif info == 'power':
            filepath = '/sys/devices/system/cpu/cpu' \
                       '{}/cpuidle/state{}/power'.format(core, state)
        elif info == 'residency':
            filepath = '/sys/devices/system/cpu/cpu' \
                       '{}/cpuidle/state{}/residency'.format(core, state)
        elif info == 'time':
            filepath = '/sys/devices/system/cpu/cpu' \
                       '{}/cpuidle/state{}/time'.format(core, state)
        elif info == 'usage':
            filepath = '/sys/devices/system/cpu/cpu' \
                       '{}/cpuidle/state{}/usage'.format(core, state)

        return self._helper.read_file_output_string(filepath)

    def set_cpuidle_state_disable(self, core, state, disable):
        """
            Option to disable this idle state.

            :param core : core number (e.g. 0).
            :param state: a state level (e.g. 2).
            :param disable : 0 == false, 1 == true
        """

        self._helper.cpu_core_validation(core)
        self._cpuidle_state_validation(core, state)

        filepath = '/sys/devices/system/cpu/cpu' \
                   '{}/cpuidle/state{}/disable'.format(core, state)

        with open(filepath, 'w') as file:
            file.write(str(disable))

    def dump_cpuidle_state(self, core):
        """
            Dump all cpuidle information for a core.

            :param core : core number (e.g. 0).
        """

        self._helper.cpu_core_validation(core)
        valid_info = ['desc', 'disable', 'latency', 'name', 'power',
                      'residency', 'time', 'usage']

        print("cpuidle dump of the core '{}'").format(core)
        print("{:=<30}\n".format('='))

        num = self.get_cpuidle_state_levels()
        for i in range(num):
            print("State idle #{}".format(i))
            for info in valid_info:
                ret = self.get_cpuidle_state_info(info, core, i)
                print('{}{} is: {}'.format('  ', info, ret))
