# script to enable mass storage & ethernet OTG gadget manually
# tested on the Orange Pi Prime

# env variables
: ${MINIMAL_IMAGE=/home/root/maschine-image-minimal-x86-congatec-sda.wic}
: ${IP=192.168.0.10}

modprobe libcomposite
cd /sys/kernel/config/usb_gadget
mkdir g1
cd g1
mkdir configs/c.1
mkdir functions/mass_storage.0
echo ${MINIMAL_IMAGE} > functions/mass_storage.0/lun.0/file
mkdir functions/ecm.usb0
mkdir strings/0x409
mkdir configs/c.1/strings/0x409
echo "0x1d6b" > idVendor
echo "0x0104" > idProduct
ls strings/0x409/
echo "0123456789" > strings/0x409/serialnumber
echo "Native Instruments GmbH" > strings/0x409/manufacturer
echo "DTFB Gadget" > strings/0x409/product
echo "Conf 1" > configs/c.1/strings/0x409/configuration
echo 250 > configs/c.1/MaxPower
echo "BE:EF:15:DE:AD:11" > /sys/kernel/config/usb_gadget/g1/functions/ecm.usb0/dev_addr
echo "BE:EF:15:DE:AD:11" > /sys/kernel/config/usb_gadget/g1/functions/ecm.usb0/host_addr
ln -s functions/mass_storage.0 configs/c.1
ln -s functions/ecm.usb0 configs/c.1
ls /sys/class/udc > UDC
ifconfig usb0 ${IP}
