#!/bin/sh
#set -x

dropbear_conf_file=/config/dropbear

led_blink_prog=led-blink

led_blink_run_file=/var/run/led-blink.run

lock_file=/var/run/lighttpd_services.cgi

input=`cat /dev/stdin`

get_current_status()
{
    # Check current status
    NO_START=0

    if [ -f $dropbear_conf_file ] ; then
	. $dropbear_conf_file
    fi
    
    # first json member
    if [ $NO_START -eq 1 ] ; then
	echo "{"
	echo "\"ssh_on\" : false,"
    else
	echo "{"
	echo "\"ssh_on\" : true,"
    fi
    
    # add new members between this line

    # and this line

    # last json member
    pidof $led_blink_prog > /dev/null
    if [ $? -eq 0 ] ; then
	if [ -f $led_blink_run_file ] ; then
	    time_left=`cat $led_blink_run_file`
	else
	    time_left=0
	fi
	echo "\"light_on\" : true,"
	echo "\"time_left\" : $time_left"
	echo "}"
    else
	echo "\"light_on\" : false"
	echo "}"
    fi
}

if [ ! -f $lock_file ] ; then
    touch $lock_file
else
    #wait until lock is gone
    i=0
    while [ -f $lock_file ] ; do
	i=`expr $i + 1`
	sleep 1
	if [ $i -ge 3 ] ; then
	    get_current_status
	    exit 0
	fi
    done
    touch $lock_file
fi


if [ "$input" != "null" ] && [ "$input" != "" ] ; then
    input=`echo $input | sed '
    s!{!!g
	s!}!!g
	s!"!!g
	s!:!=!g
	s! !!g
	s!,! !g'`
    OIFS=$IFS
    for i in $input ; do
	IFS="="
	set -- $i
	if [ "$1" = "ssh_on" ] ; then
	    if [ "$2" = "true" ] ; then
		echo "NO_START=0" > $dropbear_conf_file
		cp $dropbear_conf_file /etc/default/dropbear
		/etc/init.d/dropbear start > /dev/null
	    else
		/etc/init.d/dropbear stop > /dev/null
		echo "NO_START=1" > $dropbear_conf_file
		cp $dropbear_conf_file /etc/default/dropbear
	    fi
	fi
	if [ "$1" = "light_on" ] ; then
	    if [ "$2" = "true" ] ; then
		/usr/bin/find_my_miner.sh on
	    else
		/usr/bin/find_my_miner.sh off
	    fi
	fi
    done
fi
IFS=$OIFS

get_current_status

rm $lock_file >/dev/null
