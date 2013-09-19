#!/bin/sh
. ./cgi_lib.cgi

if [ -z "$QUERY_STRING" ] ; then
    show_same_page
    exit 0
fi
IFS="&"
set -- $QUERY_STRING

for i in $@; do 
    IFS="="
    set -- $i
    if [ "$1" = "ssh_on" ] && [ $2 -eq 1 ] ; then
	echo NO_START=1 > /boot/dropbear
    else
	> /boot/dropbear
    fi
done

/etc/init.d/services_config.sh > /dev/null
/etc/init.d/dropbear restart > /dev/null

show_apply_changes

exit 0
