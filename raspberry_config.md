# Raspberry Pi Configuration
This is the configuration used for the hosting raspberry pi

## Network Interface
In /etc/network/intefaces:

No changes to the loopback interface

    auto lo
    iface lo inet loopback

Configure a static ip on eth0

    iface eth0 inet static
    address 192.168.0.5
    netmask 255.255.255.0
    gateway 192.168.0.1
    dns-nameserver 8.8.8.8

## Retrive project sources
> mkdir ~/Prog
> cd ~/Prog
> git clone https://github.com/thierryme

## Install python dependencys
> sudo apt-get install && sudo apt-get update
> sudo apt-get install python-pip
> sudo pip install -r ~/Prog/tardis-rest/requirements.txt

## Consistent naming of Arduino tty
In order to have the same tty name at each reboot of the raspberry pi for each Arduino card, a special Udev rule is created.

First plug an Arduino card into an USB port.
Then retrive the KERNELS informaton with the following command:
> udevadm info -a -n /dev/ttyACM0 | grep KERNELS
Get the first line without a ':'. If for exemple you have "1-1.2.4"  then edit/create the following file accordingly:
> sudo vim /etc/udev/rules.d/99-arduino.rules

    SUBSYSTEM=="tty", KERNEL=="ttyACM*", KERNELS=="1-1.2.4", SYMLINK+="ttyACM0001"

Where 'ttyUSB00_Arduino_HUB1' is a tty name wich will refer to the port you pluged your Arduino in. Change this name to fit to your need.
Now the Arduino serial port should be accessible trough '/dev/ttyACM0001'.
Repeat this operation for each port and give an appropriate tty name (...0002).
(see: http://hintshop.ludvig.co.nz/show/persistent-names-usb-serial-devices/ or https://wiki.archlinux.org/index.php/arduino)

## Arduino dependencys
Install the ArduinoJson library
