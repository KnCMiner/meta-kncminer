#!/bin/sh

/etc/init.d/dropbear stop
rm -f /boot/dropbear
/etc/init.d/dropbear start

/etc/init.d/cgminer stop
rm -f /boot/cgminer.conf
/etc/init.d/miner_config.sh
/etc/init.d/cgminer start

rm -f /boot/lighttpd-htdigest.user
/etc/init.d/httpdpasswd.sh

rm -f /boot/network.conf
/etc/init.d/network.sh
