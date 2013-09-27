#!/bin/sh

/etc/init.d/dropbear stop
rm -f /config/dropbear
/etc/init.d/dropbear start

/etc/init.d/cgminer stop
rm -f /config/cgminer.conf
/etc/init.d/miner_config.sh
/etc/init.d/cgminer start

rm -f /config/lighttpd-htdigest.user
rm -f /config/shadow
/etc/init.d/httpdpasswd.sh

rm -f /config/network.conf
/etc/init.d/network.sh
