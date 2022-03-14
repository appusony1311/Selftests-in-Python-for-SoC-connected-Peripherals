import sys
import os
from os.path import join, dirname, pardir
sys.path.append(
    os.path.abspath(join(dirname(__file__), pardir)))

import cpuidle
import helper


idle = cpuidle.cpuidle()
h = helper.helper()

states = idle.get_cpuidle_state_levels()
cores = h.get_physical_cores()

# setting
[idle.set_cpuidle_state_disable(c, s, 1)
    for s in range(states) for c in range(cores)]

# checking
for s in range(states):
    for c in range(cores):
        if idle.get_cpuidle_state_info('disable', c, s) != '1':
            print("Not OK: c == {}; s == {}".format(c, s))

sys.path.remove(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
