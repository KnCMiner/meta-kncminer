#!/bin/sh
. ./cgi_lib.cgi
restart_cgminer=false

if [ -z "$QUERY_STRING" ] ; then
    show_same_page
    exit 0
fi
IFS="&"
set -- $QUERY_STRING

for i in $@; do 
    IFS="="
    set -- $i
    if [ "$1" = "r_mgmt_on" ] && [ $2 -eq 1 ] ; then
	sed -i 's/"api-listen" :.*/"api-listen" : true/g' /boot/cgminer.conf
    else
	sed -i 's/"api-listen" :.*/"api-listen" : false/g' /boot/cgminer.conf	
    fi
done

/etc/init.d/miner_config.sh > /dev/null
/etc/init.d/cgminer.sh restart > /dev/null

show_apply_changes

exit 0
