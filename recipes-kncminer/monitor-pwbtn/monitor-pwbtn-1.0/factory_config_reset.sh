#!/bin/sh

/etc/init.d/dropbear stop
/etc/init.d/cgminer.sh stop

#remove configuration
rm -f /config/*

# restore factory settings
/etc/init.d/kncminer_setup.sh

/etc/init.d/network.sh
/etc/init.d/dropbear start
