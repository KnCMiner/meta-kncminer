#!/bin/sh

# gpio 49 = PWR_EN
echo 49 > /sys/class/gpio/export
# P8.39 = gpio2_12 = DC/DC reset
echo 76 > /sys/class/gpio/export
echo high > /sys/class/gpio/gpio76/direction
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

echo '#!/bin/sh' > /sbin/reboot.safe
echo "lcd-message -l 2 'Rebooting...'" >> /sbin/reboot.safe
echo 'i2cset -y 1 0x24 0xb 0x6b' >> /sbin/reboot.safe
echo 'i2cset -y 1 0x24 0x16 0' >> /sbin/reboot.safe
echo 'reboot' >> /sbin/reboot.safe
chmod a+x /sbin/reboot.safe

# Turn ON red LED, turn ON green LED
echo low > /sys/class/gpio/gpio70/direction
echo low > /sys/class/gpio/gpio71/direction

echo Starting ioboard
cd /usr/bin

# Enable IO-board power
io-pwr init

# Program FPGA
program-fpga spimux.rbf
exit_code=$?

# Show IP ASAP
local_net="$(ip addr show eth0 | sed -n 's/^.*inet[[:space:]]*\([^[:space:]]*\)[[:space:]].*$/\1/p')"
local_ip=${local_net%%/*}
lcd-message -l 2 "$local_ip"

if [ ! -f /config/advanced.conf ] ; then
        ./waas -rd -o /config/advanced.conf
fi

if [[ $exit_code = 0 ]] ; then
        # Turn OFF red, Turn ON green
        echo high > /sys/class/gpio/gpio70/direction
        echo low > /sys/class/gpio/gpio71/direction

        ./waas -c /config/advanced.conf
else
        # Turn ON red, Turn OFF green
        echo low > /sys/class/gpio/gpio70/direction
        echo high > /sys/class/gpio/gpio71/direction
fi

# Show revision on the LCD
lcd-message -l 1 $(cat /etc/knc-release)
