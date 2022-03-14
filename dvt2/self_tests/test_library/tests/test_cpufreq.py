import sys
import os
from os.path import join, dirname, pardir
from unittest import mock
sys.path.append(
    os.path.abspath(join(dirname(__file__), pardir)))
import cpufreq
import helper

# dependecies
c = cpufreq.cpufreq()


###############################################################################
#                                      TEST CASES
###############################################################################
@mock.patch.object(helper.helper, 'read_file_output_string',
                   return_value="1792000")
@mock.patch.object(helper.helper, 'cpu_core_validation',
                   return_value=None)
def test_get_cpufreq_cur_freq(mock_cpu_val, mock_read_file_output_string):
    path = '/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_freq'
    cur_freq = c.get_cpufreq_cur_freq(0)

    assert cur_freq == 1792
    assert isinstance(cur_freq, int)
    mock_read_file_output_string.assert_called_once_with(path)


@mock.patch.object(helper.helper, 'read_file_output_string',
                   return_value="800000")
@mock.patch.object(helper.helper, 'cpu_core_validation',
                   return_value=None)
def test_get_cpufreq_min_freq(mock_cpu_val, mock_read_file_output_string):
    path = '/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_min_freq'
    min_freq = c.get_cpufreq_min_freq(0)

    assert min_freq == 800
    assert isinstance(min_freq, int)
    mock_read_file_output_string.assert_called_once_with(path)


@mock.patch.object(helper.helper, 'read_file_output_string',
                   return_value="2000000")
@mock.patch.object(helper.helper, 'cpu_core_validation',
                   return_value=None)
def test_get_cpufreq_max_freq(mock_cpu_val, mock_read_file_output_string):
    path = '/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq'
    max_freq = c.get_cpufreq_max_freq(0)

    assert max_freq == 2000
    assert isinstance(max_freq, int)
    mock_read_file_output_string.assert_called_once_with(path)


@mock.patch.object(helper.helper, 'read_file_output_string',
                   return_value="powersave performance")
@mock.patch.object(helper.helper, 'cpu_core_validation',
                   return_value=None)
def test_get_scaling_available_governors(mock_cpu_val,
                                         mock_read_file_output_string):
    path = '/sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors'
    govs = c.get_scaling_available_governors(0)

    assert govs[0] == "powersave"
    assert govs[1] == "performance"
    assert isinstance(govs, list)
    mock_read_file_output_string.assert_called_once_with(path)


@mock.patch.object(helper.helper, 'read_file_output_string',
                   return_value="intel_pstate")
@mock.patch.object(helper.helper, 'cpu_core_validation',
                   return_value=None)
def test_get_scaling_driver(mock_cpu_val, mock_read_file_output_string):
    path = '/sys/devices/system/cpu/cpu0/cpufreq/scaling_driver'
    drv_name = c.get_scaling_driver(0)

    assert drv_name == "intel_pstate"
    assert isinstance(drv_name, str)
    mock_read_file_output_string.assert_called_once_with(path)


@mock.patch.object(helper.helper, 'read_file_output_string',
                   return_value="powersave")
@mock.patch.object(helper.helper, 'cpu_core_validation',
                   return_value=None)
def test_get_scaling_governor(mock_cpu_val, mock_read_file_output_string):
    path = '/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor'
    gov = c.get_scaling_governor(0)

    assert gov == "powersave"
    assert isinstance(gov, str)
    mock_read_file_output_string.assert_called_once_with(path)


@mock.patch.object(helper.helper, 'read_file_output_string',
                   return_value="1800000")
@mock.patch.object(helper.helper, 'cpu_core_validation',
                   return_value=None)
def test_get_scaling_max_freq(mock_cpu_val, mock_read_file_output_string):
    path = '/sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq'
    freq = c.get_scaling_max_freq(0)

    assert freq == 1800
    assert isinstance(freq, int)
    mock_read_file_output_string.assert_called_once_with(path)


@mock.patch.object(helper.helper, 'read_file_output_string',
                   return_value="800000")
@mock.patch.object(helper.helper, 'cpu_core_validation',
                   return_value=None)
def test_get_scaling_min_freq(mock_cpu_val, mock_read_file_output_string):
    path = '/sys/devices/system/cpu/cpu0/cpufreq/scaling_min_freq'

    freq = c.get_scaling_min_freq(0)

    assert freq == 800
    assert isinstance(freq, int)
    mock_read_file_output_string.assert_called_once_with(path)


@mock.patch.object(helper.helper, 'read_file_output_string',
                   return_value="1792000")
@mock.patch.object(helper.helper, 'cpu_core_validation',
                   return_value=None)
def test_get_scaling_cur_freq(mock_cpu_val, mock_read_file_output_string):
    path = '/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq'

    freq = c.get_scaling_cur_freq(0)

    assert freq == 1792
    assert isinstance(freq, int)
    mock_read_file_output_string.assert_called_once_with(path)


@mock.patch.object(helper.helper, 'cpu_core_validation',
                   return_value=True)
@mock.patch('builtins.open')
def test_set_scaling_governor(m_open, mock_cpu_core):
    path = '/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor'

    gov = 'powersave'
    c.set_scaling_governor(0, gov)

    m_open.assert_has_calls([mock.call(path, 'w'),
                             mock.call().__enter__(),
                             mock.call().__enter__().write(gov),
                             mock.call().__exit__(None, None, None)])
    m_open.assert_called_once_with(path, 'w')


@mock.patch.object(helper.helper, 'cpu_core_validation',
                   return_value=True)
@mock.patch('builtins.open')
def test_set_scaling_max_freq(m_open, mock_cpu_core):
    path = '/sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq'

    freq = 1800
    c.set_scaling_max_freq(0, freq)

    m_open.assert_has_calls([mock.call(path, 'w'),
                             mock.call().__enter__(),
                             mock.call().__enter__().write(str(freq * 1000)),
                             mock.call().__exit__(None, None, None)])
    m_open.assert_called_once_with(path, 'w')


@mock.patch.object(helper.helper, 'cpu_core_validation',
                   return_value=True)
@mock.patch('builtins.open')
def test_set_scaling_min_freq(m_open, mock_cpu_core):
    path = '/sys/devices/system/cpu/cpu0/cpufreq/scaling_min_freq'

    freq = 800
    c.set_scaling_min_freq(0, freq)

    m_open.assert_has_calls([mock.call(path, 'w'),
                             mock.call().__enter__(),
                             mock.call().__enter__().write(str(freq * 1000)),
                             mock.call().__exit__(None, None, None)])
    m_open.assert_called_once_with(path, 'w')


@mock.patch.object(helper.helper, 'cpu_core_validation',
                   return_value=True)
@mock.patch('builtins.open')
def test_set_scaling_cur_freq(m_open, mock_cpu_core):
    path = '/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq'

    freq = 1795
    c.set_scaling_cur_freq(0, freq)

    m_open.assert_has_calls([mock.call(path, 'w'),
                             mock.call().__enter__(),
                             mock.call().__enter__().write(str(freq * 1000)),
                             mock.call().__exit__(None, None, None)])
    m_open.assert_called_once_with(path, 'w')
