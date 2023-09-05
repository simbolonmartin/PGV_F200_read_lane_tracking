add  file "pgv-f200-line-sensor.rules" to /etc/udev/rules.d/
This file function is to provide a symbolic link tothe usb. Edit idVendor and Product Id

according to the tutorial on: https://stackoverflow.com/questions/48356223/how-can-i-avoid-flipping-between-ttyusb0-and-ttyusb1-when-reconnecting-to-usb-po


***
You could try creating a udev rule that would create a symbolic link to that USB device and then you would be able to use something like /dev/myUSB that would always stay the same for that specific USB device.

First, you will need to find some identifying information for the USB drive. Typing in lsusb should display some information that looks like:

Bus 001 Device 004: ID 0403:6001 Future Technology Devices International
In this example 0403 is the Vendor Id and 6001 is the Product Id.

Create a file named 99_usbdevice.rules (I don't think the name matters, just the directory):

sudo nano /etc/udev/rules.d/99_usbdevices.rules
Note that the directory above may be specific to Raspbian.

Copy/paste the line below into the file and save it:

SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", SYMLINK+="myUSB"
Restart your Raspberry Pi or unplug the USB and reinsert it. There should now be a /dev/myUSB entry that you can use the same way you would the ttyUSB# entry.
***