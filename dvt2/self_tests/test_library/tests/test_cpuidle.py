import sys
import os
from pytest import raises
from os.path import join, dirname, pardir
from unittest import mock
sys.path.append(
    os.path.abspath(join(dirname(__file__), pardir)))
import cpuidle
import helper

c = cpuidle.cpuidle()


###############################################################################
#                                      TEST CASES
###############################################################################
@mock.patch.object(helper.helper, 'read_file_output_string',
                   return_value="intel_idle")
def test_get_cpuidle_cur_driver(mock_read_file_output_string):
    filepath = '/sys/devices/system/cpu/cpuidle/current_driver'

    cur_driver = c.get_cpuidle_cur_driver()
    mock_read_file_output_string.assert_called_once_with(filepath)

    assert isinstance(cur_driver, str)
    assert cur_driver == 'intel_idle'


@mock.patch.object(helper.helper, 'read_file_output_string',
                   return_value="menu")
def test_get_cpuidle_cur_governor(mock_read_file_output_string):
    filepath = '/sys/devices/system/cpu/cpuidle/current_governor_ro'

    cur_gov = c.get_cpuidle_cur_governor()
    mock_read_file_output_string.assert_called_once_with(filepath)

    assert isinstance(cur_gov, str)
    assert cur_gov == 'menu'


@mock.patch('cpuidle.listdir')
@mock.patch.object(helper.helper, 'cpu_core_validation',
                   return_value=True)
def test_get_cpuidle_state_levels(mock_read_file_output_string,
                                  mock_listdir):

    dirpath = '/sys/devices/system/cpu/cpu0/cpuidle'
    mock_listdir.return_value = ["state0", "state1",
                                 "state2", "state3", "state4"]

    num_states = c.get_cpuidle_state_levels()
    mock_listdir.assert_called_once_with(dirpath)

    assert num_states == 5
    assert isinstance(num_states, int)


@mock.patch.object(helper.helper, 'cpu_core_validation',
                   return_value=True)
@mock.patch.object(cpuidle.cpuidle, '_cpuidle_state_validation',
                   return_value=True)
@mock.patch.object(helper.helper, 'read_file_output_string')
def test_get_cpuidle_state_info(mock_read_file_output_string,
                                mock_cpuidle_validation,
                                mock_cpu_core_validation):

    # test raises
    with raises(Exception):
        c.get_cpuidle_state_info("test", 0, 4)
    with raises(Exception):
        c.get_cpuidle_state_info(12312, 0, 4)
    with raises(Exception):
        c.get_cpuidle_state_info("bal223", 0, 4)

    mock_read_file_output_string.return_value = "something1"
    info = "desc"
    filepath = '/sys/devices/system/cpu/cpu0/cpuidle/state0/desc'
    info_return = c.get_cpuidle_state_info(info, 0, 0)
    mock_read_file_output_string.assert_any_call(filepath)
    assert info_return == "something1"

    mock_read_file_output_string.return_value = "something2"
    info = "disable"
    filepath = '/sys/devices/system/cpu/cpu1/cpuidle/state0/disable'
    info_return = c.get_cpuidle_state_info(info, 1, 0)
    mock_read_file_output_string.assert_any_call(filepath)
    assert info_return == "something2"

    mock_read_file_output_string.return_value = "something3"
    info = "latency"
    filepath = '/sys/devices/system/cpu/cpu0/cpuidle/state1/latency'
    info_return = c.get_cpuidle_state_info(info, 0, 1)
    mock_read_file_output_string.assert_any_call(filepath)
    assert info_return == "something3"

    mock_read_file_output_string.return_value = "something4"
    info = "name"
    filepath = '/sys/devices/system/cpu/cpu3/cpuidle/state2/name'
    info_return = c.get_cpuidle_state_info(info, 3, 2)
    mock_read_file_output_string.assert_any_call(filepath)
    assert info_return == "something4"

    mock_read_file_output_string.return_value = "something5"
    info = "power"
    filepath = '/sys/devices/system/cpu/cpu3/cpuidle/state4/power'
    info_return = c.get_cpuidle_state_info(info, 3, 4)
    mock_read_file_output_string.assert_any_call(filepath)
    assert info_return == "something5"

    mock_read_file_output_string.return_value = "something6"
    info = "residency"
    filepath = '/sys/devices/system/cpu/cpu0/cpuidle/state4/residency'
    info_return = c.get_cpuidle_state_info(info, 0, 4)
    mock_read_file_output_string.assert_any_call(filepath)
    assert info_return == "something6"

    mock_read_file_output_string.return_value = "something7"
    info = "time"
    filepath = '/sys/devices/system/cpu/cpu0/cpuidle/state4/time'
    info_return = c.get_cpuidle_state_info(info, 0, 4)
    mock_read_file_output_string.assert_any_call(filepath)
    assert info_return == "something7"

    mock_read_file_output_string.return_value = "something8"
    info = "usage"
    filepath = '/sys/devices/system/cpu/cpu1/cpuidle/state2/usage'
    info_return = c.get_cpuidle_state_info(info, 1, 2)
    mock_read_file_output_string.assert_any_call(filepath)
    assert info_return == "something8"


@mock.patch.object(helper.helper, 'cpu_core_validation',
                   return_value=True)
@mock.patch.object(cpuidle.cpuidle, '_cpuidle_state_validation',
                   return_value=True)
@mock.patch('builtins.open')
def test_set_cpuidle_state_disable(mock_open,
                                   mock_cpuidle_validation,
                                   mock_cpu_core_validation):

    path = '/sys/devices/system/cpu/cpu0/cpuidle/state0/disable'

    c.set_cpuidle_state_disable(0, 0, 0)

    mock_open.assert_has_calls([mock.call(path, 'w'),
                                mock.call().__enter__(),
                                mock.call().__enter__().write(str(0)),
                                mock.call().__exit__(None, None, None)])
    mock_open.assert_called_once_with(path, 'w')
