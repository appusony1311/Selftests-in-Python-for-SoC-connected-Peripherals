# INSTRUCTIONS TO SET IT UP

Copy this folder to the board, e.g.:

`scp -r /this/folder root@10.1.9.21:/home/root`

Run the script: `setup.sh`

From now on, everytime you are reboot the system, the system will start this service.
Now you can do:

* Status: `systemctl status cooling_validation.service`
* Stop `systemctl stop cooling_validation.service`
* Start `systemctl start cooling_validation.service`


If you no longer want to run it in the startup, you can disable it:
`systemctl disable cooling_validation.service`

# How it works 

It creates a service that will stress the CPU while writing the temperature in a file.

* PERIOD == 1s
* FILE LOCATION == ~ (/home/root in the boards)
* CPU NUMBERS == 4


# Useful links

* https://www.kernel.org/doc/Documentation/thermal/sysfs-api.txt
* https://www.kernel.org/doc/Documentation/hwmon/sysfs-interface
