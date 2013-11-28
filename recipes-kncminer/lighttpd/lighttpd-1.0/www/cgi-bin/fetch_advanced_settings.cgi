#!/bin/sh
#set -x

trap atexit 0

lock_file=/var/run/lighttpd_advanced.cgi

asic_stat_file=/var/run/stats.knc

input=`cat /dev/stdin`

atexit() {
	rm -f $lock_file 2&> /dev/null
}

get_current_config()
{
    if [ ! -f /config/advanced.conf ] ; then
	#let waas  create conf file with defaults
	waas -d -o /config/advanced.conf
    fi
    cat /config/advanced.conf
}

if [ ! -f $lock_file ] ; then
    touch $lock_file 2&> /dev/null
else
    #wait until lock is gone
    i=0
    while [ -f $lock_file ] ; do
	i=`expr $i + 1`
	sleep 1
	if [ $i -ge 3 ] ; then
	    get_current_config
	    exit 0
	fi
    done
    touch $lock_file 2&> /dev/null
fi

fetch_advanced_settings_and_ranges()
{
    echo "{"

    # valid_ranges
    waas -i valid-ranges
    echo ","
    
    # enabled asics
    echo "\"enabled_asics\" : "
    echo "["
    if [ -f $asic_stat_file ] ; then
	i=0

	OIFS=$IFS
	IFS="="
	noof_enabled=`cat $asic_stat_file|grep asic|grep -v OFF|wc -l`
	while read status ; do
	    set -- $status
	    if [ "$1" != "" ] ; then  
		if [ "$2" != "OFF" ] ; then
		    i=`expr $i + 1`
		    if [ $i -lt $noof_enabled ] ; then
			 echo "\"$1\", "
		    else
			 echo "\"$1\""
		    fi
		fi
	    fi
	    
	done <  $asic_stat_file
	IFS=$OIFS
    fi
    echo "],"
	
    # current status
    echo "\"current_status\" : "
    waas -g all-asic-info 
    echo ","

    # current settings
    echo "\"current_settings\" : "

    get_current_config

    echo "}"
}

if [ "$input" = "fetch-advanced-settings-and-ranges" ] ; then
    fetch_advanced_settings_and_ranges
elif [ "$input" = "FactoryDefault" ] ; then
    rm -f /config/advanced.conf 2&> /dev/null
    killall monitordcdc      
    get_current_config
elif [ "$input" = "get-current-status" ] ; then
    waas -g all-asic-info 
elif [ "$input" != "null" ] && [ "$input" != "" ] ; then
    echo "$input" > /config/advanced.conf
    # let waas apply settings
    waas -c /config/advanced.conf > /dev/null
    killall monitordcdc      
    get_current_config
fi

rm $lock_file 2&> /dev/null
