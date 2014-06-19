#!/bin/sh
#set -x

trap atexit 0

lock_file=/var/run/lighttpd_advanced.cgi

input=`cat /dev/stdin`

atexit() {
	rm -f $lock_file >/dev/null 2>&1
}

get_current_config()
{
    if [ ! -f /config/advanced.conf ] ; then
	#let waas  create conf file with defaults
	waas -d -o /config/advanced.conf >/dev/null 2>&1
    fi
    cat /config/advanced.conf
}

if [ ! -f $lock_file ] ; then
    touch $lock_file >/dev/null 2>&1
fi

fetch_advanced_settings_and_ranges()
{
    echo "{"

    # valid_ranges
    waas -i valid-ranges

    . /etc/revision

    echo ","
    
    # enabled asics
    echo -n "\"enabled_asics\" : "
    sep=""
    echo -n "["
    for a in 0 1 2 3 4 5; do
	if eval test \$BOARD$a != OFF; then
	    echo -n $sep
	    echo -n "\"asic$((a+1))\""
	    sep=", "
	fi
    done
    echo "],"
	
    # current status
    echo -n "\"current_status\" : "
    waas -g all-asic-info 
    echo ","

    # current settings
    echo -n "\"current_settings\" : "

    get_current_config

    echo "}"
}

if [ "$input" = "fetch-advanced-settings-and-ranges" ] ; then
    fetch_advanced_settings_and_ranges
elif [ "$input" = "FactoryDefault" ] ; then
    rm -f /config/advanced.conf >/dev/null 2>&1
    killall monitordcdc >/dev/null 2>&1
    killall monitordcdc.ge >/dev/null 2>&1
    killall monitordcdc.ericsson >/dev/null 2>&1
    get_current_config
elif [ "$input" = "get-current-status" ] ; then
    waas -g all-asic-info 
elif [ "$input" = "recreate-config-file" ] ; then
    waas -r -o /config/advanced.conf
    get_current_config
elif [ "$input" != "null" ] && [ "$input" != "" ] ; then
    echo "$input" > /config/advanced.conf
    # let waas apply settings
    waas -c /config/advanced.conf >/dev/null 2>&1
    killall monitordcdc >/dev/null 2>&1
    killall monitordcdc.ge >/dev/null 2>&1
    killall monitordcdc.ericsson >/dev/null 2>&1
    get_current_config
fi

rm $lock_file >/dev/null 2>&1
