import dbus
from collections import namedtuple


class dbus_systemd(object):
    """
        Class to interact with systemd through dbus.

        More info:
+        [1] https://www.freedesktop.org/wiki/Software/systemd/dbus/
+        [2] https://www.digitalocean.com/community/tutorials/ \
         understanding-systemd-units-and-unit-files
+        [3] https://www.freedesktop.org/wiki/IntroductionToDBus/
+        [4] https://www.freedesktop.org/wiki/Software/DbusProjects/

    """

    def __init__(self):
        self.BUS = dbus.SystemBus()
        self.BUS_NAME = 'org.freedesktop.systemd1'
        self.BUS_PATH = '/org/freedesktop/systemd1'
        # systemd manager interface name
        self.MANAGER_IF_NAME = 'org.freedesktop.systemd1.Manager'
        # systemd unit interface name
        self.UNIT_IF_NAME = 'org.freedesktop.systemd1.Unit'
        # systemd manager object
        self.MANAGER_OBJ = self.BUS.get_object(self.BUS_NAME, self.BUS_PATH)
        # systemd manager interface
        self.MANAGER_IF = dbus.Interface(self.MANAGER_OBJ,
                                         self.MANAGER_IF_NAME)

    def get_unit_info(self, name):
        """
            Get the first unit info with its primary name containing `name`.

            It returns namedtuple object with unit info. `None` otherwise.

            :param name : String containing a unit name.
            :return namedtuple or None.

            The namedtuple attributes can be accessed by:
              nametupled.private_name
              nametupled.description
              nametupled.load_state
              nametupled.active_state
              nametupled.substate
              nametupled.object_path

            ListUnits() returns an array with all currently loaded units.
            Note that units may be known by multiple names at the same name,
            and hence there might be more unit names loaded than actual units
            behind them. The array consists of structures with the following
            elements:
            [0] The primary unit name as string
            [1] The human readable description string
            [2] The load state (i.e. whether the unit file has been loaded
                successfully)
            [3] The active state (i.e. whether the unit is currently
                started or not)
            [4] The sub state (a more fine-grained version of the active
                state that is specific to the unit type, which the active
                state is not)
            [6] The unit object path
        """

        unit_s = namedtuple('UnitInfo', ['primary_name', 'description',
                                         'load_state', 'active_state',
                                         'substate', 'object_path'])

        # Getting a list of Unit paths
        list_units = self.MANAGER_IF.ListUnits()
        for unit in list_units:
            if name in unit[0]:
                return unit_s(unit[0], unit[1], unit[2],
                              unit[3], unit[4], unit[6])

        return None

    def _timestamp_to_sec(self, timestamp):
        """
            Convert 64 bits usec timestamp to integer 32 bits timestamps.
        """

        return int(timestamp // pow(10, 6))

    def get_unit_timestamps(self, unit_path):
        """
            Get Unit Status Timestamps in seconds (standart 32 bits timestamp).

            It retuns a namedtuple object.

            The namedtuple attributes can be accessed by:
              nametupled.InactiveExitTimestamp
              nametupled.ActiveEnterTimestamp
              nametupled.ActiveExitTimestamp
              nametupled.InactiveEnterTimestamp

            Last time a unit left the inactive state, entered the active state,
            exited the active state, or entered an inactive state.
            These are the points in time where the unit transitioned:
               inactive/failed -> activating,
               activating -> active,
               active -> deactivating,
               deactivating -> inactive/failed.

            The fields are 0 in case such a transition has not been
            recording on this boot yet.

            :param : Unit object path
            :return a namedtuple or None if `unit_path` not found.
        """

        unit_ts_s = namedtuple('UnitTimestamps', ['InactiveExitTimestamp',
                                                  'ActiveEnterTimestamp',
                                                  'ActiveExitTimestamp',
                                                  'InactiveEnterTimestamp'])

        try:
            unit_object = self.BUS.get_object(self.BUS_NAME, unit_path)
        except Exception:
            print("Resolving the well-known name to a unique name fails")
            print("unit_path = `{}`".format(unit_path))
            return None

        # dbus interface
        # https://dbus.freedesktop.org/doc/dbus-java/api/org/\
        # freedesktop/DBus.Properties.html
        dbus_if = dbus.Interface(unit_object,
                                 'org.freedesktop.DBus.Properties')

        InactiveExitTimestamp = dbus_if.Get(self.UNIT_IF_NAME,
                                            'InactiveExitTimestamp')
        ActiveEnterTimestamp = dbus_if.Get(self.UNIT_IF_NAME,
                                           'ActiveEnterTimestamp')
        ActiveExitTimestamp = dbus_if.Get(self.UNIT_IF_NAME,
                                          'ActiveExitTimestamp')
        InactiveEnterTimestamp = dbus_if.Get(self.UNIT_IF_NAME,
                                             'InactiveEnterTimestamp')

        InactiveExitTimestamp = self._timestamp_to_sec(InactiveExitTimestamp)
        ActiveEnterTimestamp = self._timestamp_to_sec(ActiveEnterTimestamp)
        ActiveExitTimestamp = self._timestamp_to_sec(ActiveExitTimestamp)
        InactiveEnterTimestamp = self._timestamp_to_sec(InactiveEnterTimestamp)

        return unit_ts_s(InactiveExitTimestamp, ActiveEnterTimestamp,
                         ActiveExitTimestamp, InactiveEnterTimestamp)

    def _check_unit_none(self, info):
        if info is None:
            raise Exception("No unit found containing name `{}`".format(info))

    def get_unit_load_state(self, name):
        """
            Get unit load state. (e.g. loaded)

            It returns a namedtuple (from get_unit_info) or None.

            :param name : Unit name (String)
        """

        unit_info = self.get_unit_info(name)
        self._check_unit_none(unit_info)

        return unit_info.load_state

    def get_unit_active_state(self, name):
        """
            Get unit active state. (e.g. active)

            It returns a namedtuple (from get_unit_info) or None.

            :param name : Unit name (String)
        """

        unit_info = self.get_unit_info(name)
        self._check_unit_none(unit_info)

        return unit_info.active_state

    def get_unit_substate(self, name):
        """
            Get unit substate. (e.g. running)

            It returns a namedtuple (from get_unit_info) or None.

            :param name : Unit name (String)
        """

        unit_info = self.get_unit_info(name)
        self._check_unit_none(unit_info)

        return unit_info.substate
