#!/bin/sh

IFS="&"
set -- $QUERY_STRING

for i in $@; do 
    IFS="="
    set -- $i
    if [ "$1" = "ssh_on" ] && [ $2 -eq 1 ] ; then
	echo NO_START=1 > /config/dropbear
    else
	> /config/dropbear
    fi
done

/etc/init.d/dropbear stop > /dev/null
cp /config/dropbear /etc/default/dropbear
/etc/init.d/dropbear start > /dev/null

./get_services_conf.cgi

exit 0
