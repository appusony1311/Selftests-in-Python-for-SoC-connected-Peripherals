# removing any previous module
/sbin/modprobe -r usb_f_mass_storage

# including modules
echo peripheral > /sys/bus/platform/devices/intel-mux-drcfg/portmux.0/state
/sbin/modprobe dwc3
/sbin/modprobe dwc3_pci
/sbin/modprobe libcomposite
/sbin/modprobe usb_f_mass_storage