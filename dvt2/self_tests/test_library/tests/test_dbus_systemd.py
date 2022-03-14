import sys
import os
from pytest import raises
from os.path import join, dirname, pardir
sys.path.append(
    os.path.abspath(join(dirname(__file__), pardir)))
import dbus_systemd

dbus_s = dbus_systemd.dbus_systemd()


###############################################################################
#                                      TEST CASES
###############################################################################
def test__timestamp_to_sec():
    ts = dbus_s._timestamp_to_sec(566455139129676)
    assert isinstance(ts, int)
    assert ts == 566455139


def test__check_unit_none():
    # should return none
    text = "test"
    ret = dbus_s._check_unit_none(text)
    assert ret is None

    # should raise exception
    with raises(Exception):
        dbus_s._check_unit_none(None)
