import sys
import os
import subprocess
from pytest import raises
from unittest import mock
from os.path import join, dirname, pardir
sys.path.append(
    os.path.abspath(join(dirname(__file__), pardir)))
import helper


h = helper.helper()


###############################################################################
#                                      TEST CASES
###############################################################################
@mock.patch.object(helper.helper, 'get_physical_cores', return_value=4)
def test_cpu_core_validation(mock_cores):

    with raises(TypeError):
        h.cpu_core_validation("4")

    with raises(TypeError):
        h.cpu_core_validation("dasdsa")

    with raises(ValueError):
        h.cpu_core_validation(4)

    with raises(ValueError):
        h.cpu_core_validation(-1)

    # if successfully should return None
    assert h.cpu_core_validation(0) is None


@mock.patch.object(helper.helper, 'execute_cmd_output_string')
def test_is_maschine_usb_detected(mock_execute):
    # to pass
    for device in ['17cc:1600', '17cc:1820']:
        mock_execute.return_value = device
        detected = h.is_maschine_usb_detected()
        mock_execute.assert_called_with('lsusb')
        assert detected is True

    # to fail
    device = '17cc:1800'
    mock_execute.return_value = device
    detected = h.is_maschine_usb_detected()
    mock_execute.assert_called_with('lsusb')
    assert detected is False


@mock.patch.object(helper.helper, 'execute_cmd_output_string')
def test_is_maschine_alsa_detected(mock_execute):

    mock_execute.return_value = 'MK3 [Maschine MK3], device 0: ' \
                                'USB Audio [USB Audio]'

    detected = h.is_maschine_alsa_detected()
    mock_execute.assert_called_with('aplay -l')
    assert detected is True

    mock_execute.return_value = 'Maschine blabla'
    detected = h.is_maschine_alsa_detected()
    mock_execute.assert_called_with('aplay -l')
    assert detected is False


def test_is_integer_value():
    with raises(TypeError):
        h.is_integer_value(0.0)

    with raises(TypeError):
        h.is_integer_value("0")

    with raises(TypeError):
        h.is_integer_value("asb")

    for value in [123, 0, -231]:
        ret = h.is_integer_value(value)
        assert ret is None


@mock.patch('helper.subprocess.call')
def test_execute_cmd_output_file(mock_subprocess):
    mock_subprocess.return_value = 0
    ret = h.execute_cmd_output_file("cmd", "output")

    assert ret == "/tmp/test_lib/output"
    assert isinstance(ret, str)

    mock_subprocess.return_value = 1
    with raises(AssertionError):
        h.execute_cmd_output_file("cmd", "output")


@mock.patch('helper.subprocess.check_output')
def test_execute_cmd_output_string(mock_subprocess):
    mock_subprocess.return_value = b"blabla"
    ret = h.execute_cmd_output_string("cmd")

    assert ret == "blabla"
    assert isinstance(ret, str)

    mock_subprocess.side_effect = subprocess.CalledProcessError(0, "hi", "no")
    with raises(AssertionError):
        h.execute_cmd_output_string("cmd")


@mock.patch('helper.subprocess.call')
def test_execute_cmd_return_code(mock_subprocess):
    mock_subprocess.return_value = 0
    ret = h.execute_cmd_return_code("cmd")
    assert ret == 0

    mock_subprocess.return_value = 1
    ret = h.execute_cmd_return_code("cmd")
    assert ret == 1


@mock.patch.object(helper.helper, 'execute_cmd_output_string')
def test_execute_ssh_output_list(mock_execute):
    msg = ["bla\nbla\n", "bla"]
    for m in msg:
        mock_execute.return_value = m
        assert mock_execute.return_value == m
        ret = h.execute_ssh_output_list('10.1.9.20', 'cmd')
        assert ret == m.split("\n")[1:]
        assert isinstance(ret, list)


@mock.patch.object(helper.helper, 'execute_cmd_return_code')
def test_execute_ssh_return_code(mock_execute):
    codes = [0, 1]
    for code in codes:
        mock_execute.return_value = code
        assert mock_execute.return_value == code
        ret = h.execute_ssh_return_code('10.1.9.20', 'cmd')
        assert ret == code


@mock.patch('helper.isfile')
def test_read_file_output_string(mock_isfile):
    somepath = "some/path"
    mock_isfile.return_value = False
    assert mock_isfile.return_value is False
    with raises(IOError):
        h.read_file_output_string(somepath)
        mock_isfile.assert_called_with(somepath)

    with mock.patch('builtins.open', mock.mock_open(read_data="test")) as m:
        mock_isfile.return_value = True
        assert mock_isfile.return_value is True
        mock_isfile.assert_called_with(somepath)
        ret = h.read_file_output_string(somepath)

    m.assert_called_with(somepath, 'r')
    assert ret == "test"


@mock.patch.object(helper.helper, 'execute_cmd_return_code')
def test_is_ping_succeeded(mock_execute):
    ip = '10.1.9.20'

    mock_execute.return_value = 0
    ret = h.is_ping_succeeded(ip)
    assert ret is True

    mock_execute.return_value = 1
    ret = h.is_ping_succeeded(ip)
    assert ret is False

    mock_execute.return_value = 100
    ret = h.is_ping_succeeded(ip)
    assert ret is False

    mock_execute.return_value = -1
    ret = h.is_ping_succeeded(ip)
    assert ret is False


@mock.patch.object(helper.helper, 'execute_ssh_return_code')
def test_system_reboot_device(mock_execute):
    ip = "10.1.9.20"
    cmd = '/sbin/reboot'

    mock_execute.return_value = 0
    assert h.system_reboot_device(ip) is None
    mock_execute.assert_called_with(ip, cmd)

    mock_execute.return_value = 1
    assert h.system_reboot_device(ip) is None
    mock_execute.assert_called_with(ip, cmd)

    mock_execute.return_value = 100
    assert h.system_reboot_device(ip) is None
    mock_execute.assert_called_with(ip, cmd)


@mock.patch.object(helper.helper, 'execute_ssh_return_code')
def test_system_shutdown_device(mock_execute):
    ip = "10.1.9.20"
    cmd = '/sbin/poweroff'

    mock_execute.return_value = 0
    assert h.system_shutdown_device(ip) is None
    mock_execute.assert_called_with(ip, cmd)

    mock_execute.return_value = 1
    assert h.system_shutdown_device(ip) is None
    mock_execute.assert_called_with(ip, cmd)

    mock_execute.return_value = 100
    assert h.system_shutdown_device(ip) is None
    mock_execute.assert_called_with(ip, cmd)


@mock.patch.object(helper.helper, 'execute_cmd_return_code')
def test_hw_reset_device(mock_execute):
    cmd = 'gpio-tool.sh reset'

    mock_execute.return_value = 0
    assert h.hw_reset_device() is None
    mock_execute.assert_called_with(cmd)

    mock_execute.return_value = 1
    assert h.hw_reset_device() is None
    mock_execute.assert_called_with(cmd)

    mock_execute.return_value = 100
    assert h.hw_reset_device() is None
    mock_execute.assert_called_with(cmd)


@mock.patch.object(helper.helper, 'execute_cmd_return_code')
def test_hw_poweroff_device(mock_execute):
    cmd = 'gpio-tool.sh poweroff'

    mock_execute.return_value = 0
    assert h.hw_poweroff_device() is None
    mock_execute.assert_called_with(cmd)

    mock_execute.return_value = 1
    assert h.hw_poweroff_device() is None
    mock_execute.assert_called_with(cmd)

    mock_execute.return_value = 100
    assert h.hw_poweroff_device() is None
    mock_execute.assert_called_with(cmd)


@mock.patch.object(helper.helper, 'execute_cmd_return_code')
def test_hw_poweron_device(mock_execute):
    cmd1 = 'gpio-tool.sh poweron'
    cmd2 = 'gpio-tool.sh reset'

    mock_execute.return_value = 0
    assert h.hw_poweron_device() is None
    mock_execute.assert_any_call(cmd1)
    mock_execute.assert_called_with(cmd2)

    mock_execute.return_value = 1
    assert h.hw_poweron_device() is None
    mock_execute.assert_any_call(cmd1)
    mock_execute.assert_called_with(cmd2)

    mock_execute.return_value = 100
    assert h.hw_poweron_device() is None
    mock_execute.assert_any_call(cmd1)
    mock_execute.assert_called_with(cmd2)


@mock.patch.object(helper.helper, 'execute_ssh_output_list')
def test_system_uptime(mock_ssh):
    ip = '10.1.9.20'
    valid_args = ['p', 's']
    hour = ["blablabla 1h30m"]

    for arg in valid_args:
        mock_ssh.return_value = hour
        ret = h.system_uptime(ip, arg)
        mock_ssh.assert_called_with(ip, '/usr/bin/uptime -{}'.format(arg))
        assert ret == hour[0]
        assert isinstance(ret, str)

    with raises(Exception):
        mock_ssh.return_value = hour
        h.system_uptime(ip, 'a')


@mock.patch.object(helper.helper, 'is_ping_succeeded')
def test_wait_until_device_is_pingable(mock_ssh):
    ip = '10.1.9.20'

    mock_ssh.return_value = True
    ret = h.wait_until_device_is_pingable(ip)
    mock_ssh.assert_called_with(ip)
    assert ret is True

    mock_ssh.return_value = False
    ret = h.wait_until_device_is_pingable(ip)
    mock_ssh.assert_called_with(ip)
    assert ret is False


@mock.patch.object(helper.helper, 'is_ping_succeeded')
def test_wait_until_device_is_not_pingable(mock_ssh):
    ip = '10.1.9.20'

    mock_ssh.return_value = True
    ret = h.wait_until_device_is_not_pingable(ip)
    mock_ssh.assert_called_with(ip)
    assert ret is False

    mock_ssh.return_value = False
    ret = h.wait_until_device_is_not_pingable(ip)
    mock_ssh.assert_called_with(ip)
    assert ret is True


@mock.patch.object(helper.helper, 'execute_cmd_output_file')
def test_get_physical_cores(mock_execute):
    mock_execute.return_value = "tests/test_data/cpuinfo"
    cores = h.get_physical_cores()

    assert cores == 4
    assert isinstance(cores, int)


@mock.patch.object(helper.helper, 'execute_cmd_output_file')
def test_get_cpu_model(mock_execute):
    mock_execute.return_value = "tests/test_data/cpuinfo"
    cores = h.get_cpu_model()

    assert cores == 42
    assert isinstance(cores, int)


@mock.patch.object(helper.helper, 'execute_cmd_output_file')
def test_get_cpu_model_name(mock_execute):
    mock_execute.return_value = "tests/test_data/cpuinfo"
    cores = h.get_cpu_model_name()

    assert cores == "Intel(R) Xeon(R) CPU E31225 @ 3.10GHz"
    assert isinstance(cores, str)


def test_get_cpu_temp():
    somepath = "/sys/class/thermal/thermal_zone0/temp"

    with mock.patch('builtins.open', mock.mock_open(read_data="58000")) as m:
        temp = h.get_cpu_temp()

    m.assert_called_with(somepath)
    assert temp == 58.0
    assert isinstance(temp, float)


def test_calculate_count_arg():
    with raises(Exception):
        h._calculate_count_arg(1024, 1024)
        h._calculate_count_arg('1k', 1024)
        h._calculate_count_arg(1024, '1M')
        h._calculate_count_arg('1g', '1k')
        h._calculate_count_arg('1k', '1z')
        h._calculate_count_arg('1i', '343243u')
        h._calculate_count_arg('1m', '2m')

    assert h._calculate_count_arg('1024', '1024') == 1
    assert h._calculate_count_arg('8k', '1024') == 8
    assert h._calculate_count_arg('1m', '1k') == 1024
    assert h._calculate_count_arg('512m', '1m') == 512
    assert h._calculate_count_arg('512m', '1m') == 512
