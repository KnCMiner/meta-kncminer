#!/bin/sh

cmd=$1
if [ "x$cmd" = "x" ]; then
	running=$(pidof led-blink)
	if [ "x$running" = "x" ]; then
		cmd=on
	else
		cmd=off
	fi
fi

if [ ! -f /config/led-blink.conf ] ; then
	echo "# default_time in seconds" > /config/led-blink.conf
	echo "default_time=600" >> /config/led-blink.conf
fi
. /config/led-blink.conf
if [ "$cmd" = "on" ]; then
	/usr/bin/led-blink $default_time > /dev/null
else
	killall led-blink > /dev/null
fi

if [ -f /config/network.conf ] ; then
	. /config/network.conf
fi
if [ "x$SNMP_COMMUNITY" = "x" ] ; then
	SNMP_COMMUNITY=public
fi
OIFS="$IFS"
IFS=" ,	"
for addr in ${SNMP_MANAGERS}; do
	/usr/bin/snmptrap -v2c -c"$SNMP_COMMUNITY" $addr "" kncMiner.traps.find-my-miner
done
IFS="$OIFS"
