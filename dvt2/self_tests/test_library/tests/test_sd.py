import sys
import os
from os.path import join, dirname, pardir
from unittest import mock
sys.path.append(
    os.path.abspath(join(dirname(__file__), pardir)))
import helper
import sd

# dependecies
mmc = sd.sd()


###############################################################################
#                                      TEST CASES
###############################################################################
@mock.patch.object(helper.helper, 'read_file_output_string',
                   return_value="29884416")
def test_get_sd_size(mock_read):

    ret = mmc.get_sd_size()

    assert ret == (29884416 * 512 / 2**20)
    assert isinstance(ret, int)

    mock_read.assert_called_with("/sys/class/block/mmcblk0/size")


@mock.patch.object(helper.helper, 'read_file_output_string',
                   return_value="0x01508880")
def test_get_sd_serial_num(mock_read):

    ret = mmc.get_sd_serial_num()

    assert ret == "0x01508880"
    assert isinstance(ret, str)

    mock_read.assert_called_with("/sys/block/mmcblk0/device/serial")


@mock.patch.object(helper.helper, 'read_file_output_string',
                   return_value="M52516")
def test_get_sd_name(mock_read):

    ret = mmc.get_sd_name()

    assert ret == "M52516"
    assert isinstance(ret, str)

    mock_read.assert_called_with("/sys/block/mmcblk0/device/name")


@mock.patch('helper.os.path.ismount')
def test_is_mount_point_exists(mock_execute):
    mock_execute.return_value = True
    ret = mmc.is_mount_point_exists("/boot")
    assert ret is True
    assert isinstance(ret, bool)
    mock_execute.assert_called_with("/boot")

    mock_execute.return_value = False
    ret = mmc.is_mount_point_exists("/mmcblk0")
    assert ret is False
    assert isinstance(ret, bool)
    mock_execute.assert_called_with("/mmcblk0")


@mock.patch.object(helper.helper, 'read_file_output_string',
                   return_value="1508880")
def test_get_size_of_mounted_partition(mock_read):

    ret = mmc.get_size_of_mounted_partition("mmcblk0p1")

    assert ret == int(1508880 * 512 / 2**20)
    assert isinstance(ret, int)

    mock_read.assert_called_with("/sys/class/block/mmcblk0p1/size")


# @mock.patch.object(helper.helper, 'read_file_output_string',
#                    return_value="1508880")
# def test_read_perf(mock_read):
#
# 	ret = mmc.read_perf("mmcblk0p1")
#
# 	assert ret == 1508880
# 	assert isinstance(ret, int)
#
