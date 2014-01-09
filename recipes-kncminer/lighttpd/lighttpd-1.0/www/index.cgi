#!/bin/sh
if [ -f /config/network.conf ]; then
	. /config/network.conf
fi
if [ "$remote_mgmt" = "" ]; then
	exec /www/pages/setup.cgi
fi

cat /www/pages/index.html
