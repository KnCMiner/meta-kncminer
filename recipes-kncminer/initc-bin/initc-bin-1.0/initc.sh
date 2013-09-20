#!/bin/sh

# gpio 49 = PWR_EN
echo 49 > /sys/class/gpio/export
# gpio2_6 = 70 = red LED
echo 70 > /sys/class/gpio/export
# gpio2_7 = 71 = green LED 
echo 71 > /sys/class/gpio/export
# P8.7 = gpio2_2 = CONF_DONE
echo 66 > /sys/class/gpio/export
echo in > /sys/class/gpio/gpio66/direction 
# P8.8 = gpio2_3 = nCONFIG
echo 67 > /sys/class/gpio/export
echo high > /sys/class/gpio/gpio67/direction
# P8.9 = gpio2_5 = nSTATUS
echo 69 > /sys/class/gpio/export
echo in > /sys/class/gpio/gpio69/direction
# gpio1_27 = clock_enable
echo 59 > /sys/class/gpio/export
echo high > /sys/class/gpio/gpio59/direction

# Turn ON red LED, turn OFF green LED
echo low > /sys/class/gpio/gpio70/direction
echo high > /sys/class/gpio/gpio71/direction

echo Starting initc
cd /usr/bin
./initc 
if [[ $? = 0 ]] ; then
	# Turn OFF red, Turn ON green
	echo high > /sys/class/gpio/gpio70/direction
	echo low > /sys/class/gpio/gpio71/direction
fi

