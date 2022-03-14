import helper

from collections import OrderedDict

class ram_info(object):
    """
        RAM memory information

    """

    def __init__(self):
        self._helper = helper.helper()

###############################################################################
# RAM info METHODS
###############################################################################

    def ram_info(self):
        ''' Return the RAM Total memory and Free memory information from /proc/meminfo
        as a dictionary '''
        meminfo = OrderedDict()

        with open('/proc/meminfo') as f:
            for line in f:
                meminfo[line.split(':')[0]] = line.split(':')[1].strip()

        MemTotal = meminfo['MemTotal'].split()

        MemFree = meminfo['MemFree'].split()

        return int(MemTotal[-2]), int(MemFree[-2])
