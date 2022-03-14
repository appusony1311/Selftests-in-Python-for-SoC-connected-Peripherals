import sys
import os
from os.path import join, dirname, pardir
from unittest import mock
sys.path.append(
    os.path.abspath(join(dirname(__file__), pardir)))
import helper
import emmc

# dependecies
mmc = emmc.emmc()


###############################################################################
#                                      TEST CASES
###############################################################################
@mock.patch.object(helper.helper, 'read_file_output_string',
                   return_value="29884416")
def test_get_emmc_size(mock_read):

    ret = mmc.get_emmc_size()

    assert ret == (29884416 * 512 / 2**20)
    assert isinstance(ret, int)

    mock_read.assert_called_with("/sys/class/block/mmcblk1/size")


@mock.patch.object(helper.helper, 'read_file_output_string',
                   return_value="0x01508880")
def test_get_emmc_serial_num(mock_read):

    ret = mmc.get_emmc_serial_num()

    assert ret == "0x01508880"
    assert isinstance(ret, str)

    mock_read.assert_called_with("/sys/block/mmcblk1/device/serial")


@mock.patch.object(helper.helper, 'read_file_output_string',
                   return_value="M52516")
def test_get_emmc_name(mock_read):

    ret = mmc.get_emmc_name()

    assert ret == "M52516"
    assert isinstance(ret, str)

    mock_read.assert_called_with("/sys/block/mmcblk1/device/name")


@mock.patch('helper.os.path.ismount')
def test_is_mount_point_exists(mock_execute):
    mock_execute.return_value = True
    ret = mmc.is_mount_point_exists("/boot")
    assert ret is True
    assert isinstance(ret, bool)
    mock_execute.assert_called_with("/boot")

    mock_execute.return_value = False
    ret = mmc.is_mount_point_exists("/mmcblk1")
    assert ret is False
    assert isinstance(ret, bool)
    mock_execute.assert_called_with("/mmcblk1")


@mock.patch.object(helper.helper, 'execute_cmd_output_string',
                   return_value="`-mmcblk0p3 179:3    0  512M  0 part [SWAP]")
def test_is_swap_present(mock_execute):

    ret = mmc.is_swap_present("[SWAP]")
    assert ret is True
    assert isinstance(ret, bool)

    ret = mmc.is_swap_present("/")
    assert ret is False
    assert isinstance(ret, bool)

    mock_execute.assert_called_with("lsblk")


@mock.patch.object(helper.helper, 'read_file_output_string',
                   return_value="1508880")
def test_get_size_of_mounted_partition(mock_read):

    ret = mmc.get_size_of_mounted_partition("mmcblk1p1")

    assert ret == int(1508880 * 512 / 2**20)
    assert isinstance(ret, int)

    mock_read.assert_called_with("/sys/class/block/mmcblk1p1/size")


# @mock.patch.object(helper.helper, 'read_file_output_string',
#                    return_value="1508880")
# def test_read_perf(mock_read):
#
# 	ret = mmc.read_perf("mmcblk1p1")
#
# 	assert ret == 1508880
# 	assert isinstance(ret, int)
#
