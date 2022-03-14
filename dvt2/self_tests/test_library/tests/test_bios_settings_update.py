import sys
import os
from unittest import mock
from os.path import join, dirname, pardir
sys.path.append(
    os.path.abspath(join(dirname(__file__), pardir)))
import helper
import bios_settings_update


# dependecies
bios_update = bios_settings_update.bios_settings_update()


###############################################################################
#                                      TEST CASES
###############################################################################
@mock.patch.object(helper.helper, 'execute_cmd_return_code')
def test_bios_settings_update(mock_execute):
    backup_map_file = '/usr/share/congatec/bios-backup-map.mod'
    default_map_file = '/usr/share/congatec/bios-default-map.mod'

    write_backup_map = 1
    write_default_map = 2

    wrong_map_file = '/usr/share/blaaaaaaaaaaaaaaaa'
    write_wrong_map = '3'

    mock_execute.return_value = 0
    ret = bios_update.bios_settings_update(backup_map_file, write_backup_map)
    assert ret is True

    mock_execute.return_value = 0
    ret = bios_update.bios_settings_update(default_map_file, write_default_map)
    assert ret is True

    mock_execute.return_value = 1
    ret = bios_update.bios_settings_update(wrong_map_file, write_wrong_map)
    assert ret is False

