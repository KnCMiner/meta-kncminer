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
    if [ "$1" = "r_mgmt_on" ] && [ $2 -eq 1 ] ; then
	sed -i 's#"api-listen".*:.* false#"api-listen" : true#g' /config/cgminer.conf
	sed -i 's#"api-network".*:.*false#"api-network" : true#g' /config/cgminer.conf
    else
	sed -i 's#"api-listen".*:.*true#"api-listen" : false#g' /config/cgminer.conf	
	sed -i 's#"api-network".*:.*true#"api-network" : false#g' /config/cgminer.conf
    fi
done

/etc/init.d/miner_config.sh > /dev/null
/etc/init.d/cgminer.sh stop > /dev/null
/etc/init.d/cgminer.sh start > /dev/null

show_apply_changes

exit 0
